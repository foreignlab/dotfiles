#!/usr/bin/env python3
"""
Auto-Compact時にCipherにメモリを保存するPythonスクリプト
PreCompact Input JSONを解析し、Cipherに会話内容を記憶させる
"""

import json
import sys
import os
import logging
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional

# 共通設定とユーティリティをインポート
from config import CIPHER_CONFIG, MESSAGE_CONFIG, PROJECT_CONFIG, LANGUAGE_PATTERNS, TASK_PATTERNS, PRIORITY_PATTERNS, STATUS_PATTERNS
from utils import setup_logging, extract_project_context, truncate_for_log, get_current_timestamp

# ログ設定
logger = setup_logging('SAVE')

def read_stdin_json() -> Optional[Dict[str, Any]]:
    """標準入力からJSONを読み取る"""
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            logger.error("No input data received from stdin")
            return None

        return json.loads(input_data)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON input: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading stdin: {e}")
        return None

def read_transcript(transcript_path: str) -> Optional[List[Dict[str, Any]]]:
    """トランスクリプトファイルを読み取る"""
    try:
        if not os.path.exists(transcript_path):
            logger.error(f"Transcript file not found: {transcript_path}")
            return None

        messages = []
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        logger.info(f"Read {len(messages)} messages from transcript")
        return messages
    except Exception as e:
        logger.error(f"Error reading transcript: {e}")
        return None

def extract_conversation_content(messages: List[Dict[str, Any]], limit: int = MESSAGE_CONFIG['default_limit']) -> str:
    """会話内容から重要な部分を抽出"""
    try:
        # 最新のメッセージから指定数を取得
        recent_messages = messages[-limit:] if len(messages) > limit else messages

        conversation_parts = []
        for msg in recent_messages:
            msg_type = msg.get('type', '')
            message_data = msg.get('message', {})

            # userまたはassistantメッセージの処理
            if msg_type in ['user', 'assistant'] and message_data:
                role = message_data.get('role', msg_type)
                content = message_data.get('content', '')

                # contentが文字列の場合
                if isinstance(content, str) and content.strip():
                    conversation_parts.append(f"[{role}]: {content}")
                # contentが配列の場合（tool_useなど）
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text = item.get('text', '')
                                if text.strip():
                                    conversation_parts.append(f"[{role}]: {text}")
                            elif item.get('type') == 'tool_use':
                                tool_name = item.get('name', 'unknown_tool')
                                conversation_parts.append(f"[{role}-tool]: {tool_name}")

        logger.info(f"Extracted {len(conversation_parts)} conversation parts from {len(recent_messages)} messages")

        # デバッグ：コンテンツが抽出されなかった場合
        if not conversation_parts and recent_messages:
            logger.warning(f"No conversation parts extracted from {len(recent_messages)} messages")
            sample_msg = recent_messages[0]
            logger.debug(f"Sample message structure: {list(sample_msg.keys())}")

        return "\n".join(conversation_parts)
    except Exception as e:
        logger.error(f"Error extracting conversation content: {e}")
        return ""

# extract_project_context は shared_utils から使用

def detect_languages(content: str) -> List[str]:
    """会話内容からプログラミング言語を検出"""
    languages = []

    # 言語パターンを設定から使用
    language_patterns = LANGUAGE_PATTERNS

    for lang, patterns in language_patterns.items():
        if any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE) for pattern in patterns):
            languages.append(lang)

    return languages if languages else ['general']

def detect_project_status(content: str) -> str:
    """プロジェクトの状況を検出"""
    content_lower = content.lower()

    for status, patterns in STATUS_PATTERNS.items():
        if patterns and any(word in content_lower for word in patterns):
            return status
    return 'active'

def generate_smart_tags(conversation_content: str, project_context: Dict[str, Any]) -> List[str]:
    """会話内容から智能的にタグを生成"""
    tags = ["auto-compact"]

    # プロジェクト関連タグ
    if project_name := project_context.get('name'):
        if project_name != 'unknown':
            tags.append(f"project:{project_name}")

    # 言語検出
    languages = detect_languages(conversation_content)
    tags.extend([f"lang:{lang}" for lang in languages])

    # タスクタイプ検出
    content_lower = conversation_content.lower()
    for task_type, patterns in TASK_PATTERNS.items():
        if any(word in content_lower for word in patterns):
            tags.append(f"task:{task_type}")
            break

    # 優先度検出
    priority_found = False
    for priority, patterns in PRIORITY_PATTERNS.items():
        if patterns and any(word in content_lower for word in patterns):
            tags.append(f"priority:{priority}")
            priority_found = True
            break
    if not priority_found:
        tags.append("priority:medium")

    # 状況タグ
    status = detect_project_status(conversation_content)
    tags.append(f"status:{status}")

    return tags

def count_messages(conversation_content: str) -> int:
    """会話メッセージ数をカウント"""
    return len([line for line in conversation_content.split('\n') if line.strip().startswith('[')])

def save_to_cipher(conversation_content: str, session_id: str, transcript_path: str) -> bool:
    """Cipherに会話内容を構造化して保存（MCP経由）"""
    try:
        timestamp = get_current_timestamp()
        project_context = extract_project_context(transcript_path)

        # 構造化されたメモリ内容
        memory_content = f"""
Claude Code Auto-Compact Memory Archive

# Session Context
- Session ID: {session_id}
- Timestamp: {timestamp}
- Event: auto-compact triggered
- Project: {project_context.get('name', 'unknown')}
- Working Directory: {project_context.get('path', 'unknown')}

# Summary Request
以下のauto-compact直前の会話内容から、次のセッションで継続作業するために必要な情報を抽出・要約して `ask_cipher` を使って記憶してください。

{conversation_content}

# Memory Extraction Instructions
## 🎯 Project Goals & Current Status
- プロジェクトの目的と現在の進捗状況を記録してください

## 📋 Active Tasks & Next Steps
- 継続中のタスクと次に実行すべきアクションを整理してください

## 🔧 Technical Context
- 重要な技術的決定や発見事項を保存してください
- 使用している技術スタックや手法を記録してください

## 📝 Important Context
- ユーザーの要求や制約条件を記憶してください
- 注意すべき事項や既知の問題を記録してください

## 🏷️ Classification Tags
以下の形式でタグ付けしてください：
- project:{project_context.get('name', 'unknown')}
- session-type:auto-compact
- language:{','.join(detect_languages(conversation_content))}
- status:{detect_project_status(conversation_content)}
        """.strip()

        # 強化されたメタデータ
        smart_tags = generate_smart_tags(conversation_content, project_context)
        metadata = {
            "sessionId": session_id,
            "source": "auto-compact",
            "projectId": project_context.get('name'),
            "timestamp": timestamp,
            "tags": smart_tags,
            "context": {
                "triggerEvent": "auto-compact",
                "messageCount": count_messages(conversation_content),
                "workingDirectory": project_context.get('path'),
                "detectedLanguages": detect_languages(conversation_content),
                "projectStatus": detect_project_status(conversation_content)
            }
        }

        logger.info(f"Enhanced memory content prepared: {len(memory_content)} characters")
        logger.info(f"Project: {project_context.get('name')}")
        logger.info(f"Languages detected: {detect_languages(conversation_content)}")
        logger.info(f"Smart tags: {smart_tags}")

        # Claude CLI経由でCipherに実際に通信
        logger.info("🔄 Attempting Cipher communication via Claude CLI...")

        try:
            # Claude CLI実行
            result = subprocess.run(
                CIPHER_CONFIG['claude_cli_command'],
                input=memory_content,
                capture_output=True,
                text=True,
                timeout=CIPHER_CONFIG['timeout_seconds']
            )

            if result.returncode == 0:
                logger.info("✅ Successfully saved to Cipher via Claude CLI")
                logger.info(f"🏷️ Smart tags applied: {smart_tags}")
                logger.info(f"📝 Memory saved: {len(memory_content)} characters")

                # レスポンスの一部をログに記録（デバッグ用）
                response_preview = truncate_for_log(result.stdout, MESSAGE_CONFIG['max_response_length'])
                logger.info(f"🔍 Cipher response: {response_preview}")

                return True
            else:
                logger.error(f"Claude CLI failed with return code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"Claude CLI timed out after {CIPHER_CONFIG['timeout_seconds']} seconds")
            return False
        except FileNotFoundError:
            logger.error("Claude CLI not found in PATH")
            return False
        except Exception as e:
            logger.error(f"Claude CLI communication failed: {e}")
            return False

    except Exception as e:
        logger.error(f"Error saving enhanced memory to Cipher: {e}")
        return False

def main():
    """メイン処理"""
    logger.info("Cipher memory save script started")

    # 標準入力からPreCompact Input JSONを読み取り
    input_data = read_stdin_json()
    if not input_data:
        logger.error("Failed to read input JSON")
        sys.exit(1)

    # triggerがautoの場合のみ処理
    trigger = input_data.get('trigger', '')
    if trigger != 'auto':
        logger.info(f"Skipping processing for trigger: {trigger}")
        sys.exit(0)

    session_id = input_data.get('session_id', 'unknown')
    transcript_path = input_data.get('transcript_path', '')

    logger.info(f"Processing auto-compact for session: {session_id}")

    # トランスクリプトファイルを読み取り
    messages = read_transcript(transcript_path)
    if not messages:
        logger.error("Failed to read transcript messages")
        sys.exit(1)

    # 会話内容を抽出
    conversation_content = extract_conversation_content(messages)
    if not conversation_content:
        logger.warning("No conversation content extracted")
        sys.exit(0)

    # Cipherに保存（transcript_pathも渡す）
    if save_to_cipher(conversation_content, session_id, transcript_path):
        logger.info("Successfully saved conversation to Cipher")
        sys.exit(0)
    else:
        logger.error("Failed to save conversation to Cipher")
        sys.exit(1)

if __name__ == "__main__":
    main()