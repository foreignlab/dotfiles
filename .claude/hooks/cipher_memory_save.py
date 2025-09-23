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
from datetime import datetime
from typing import Dict, List, Any, Optional

# ログ設定
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'cipher_hook.log')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

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

def extract_conversation_content(messages: List[Dict[str, Any]], limit: int = 20) -> str:
    """会話内容から重要な部分を抽出"""
    try:
        # 最新のメッセージから指定数を取得
        recent_messages = messages[-limit:] if len(messages) > limit else messages

        conversation_parts = []
        for msg in recent_messages:
            msg_type = msg.get('type', '')
            content = msg.get('content', '')

            if msg_type == 'text' and content:
                # ユーザーまたはアシスタントのテキストメッセージ
                role = msg.get('role', 'unknown')
                conversation_parts.append(f"[{role}]: {content}")
            elif msg_type == 'tool_use':
                # ツール使用の記録
                tool_name = msg.get('name', 'unknown_tool')
                conversation_parts.append(f"[tool]: {tool_name}")

        return "\n".join(conversation_parts)
    except Exception as e:
        logger.error(f"Error extracting conversation content: {e}")
        return ""

def extract_project_context(transcript_path: str) -> Dict[str, Any]:
    """トランスクリプトパスからプロジェクトコンテキストを抽出"""
    try:
        # パスからプロジェクト名を推測
        path_parts = transcript_path.split('/')
        project_name = "unknown"
        working_dir = "unknown"

        # プロジェクトディレクトリを探す
        for i, part in enumerate(path_parts):
            if part in ['Documents', 'Projects', 'workspace', 'code']:
                if i + 1 < len(path_parts):
                    project_name = path_parts[i + 1]
                    working_dir = '/'.join(path_parts[:i + 2])
                break

        return {
            "name": project_name,
            "path": working_dir,
            "transcript_path": transcript_path
        }
    except Exception as e:
        logger.error(f"Error extracting project context: {e}")
        return {"name": "unknown", "path": "unknown", "transcript_path": transcript_path}

def detect_languages(content: str) -> List[str]:
    """会話内容からプログラミング言語を検出"""
    languages = []

    # 一般的な言語パターン
    language_patterns = {
        'python': [r'\.py\b', r'python', r'pip\s+install', r'def\s+\w+', r'import\s+\w+'],
        'javascript': [r'\.js\b', r'\.ts\b', r'npm\s+install', r'function\s+\w+', r'const\s+\w+'],
        'java': [r'\.java\b', r'public\s+class', r'package\s+\w+', r'import\s+java'],
        'go': [r'\.go\b', r'func\s+\w+', r'package\s+main', r'import\s+"'],
        'rust': [r'\.rs\b', r'fn\s+\w+', r'use\s+std::', r'cargo\s+'],
        'shell': [r'\.sh\b', r'#!/bin/bash', r'chmod\s+\+x', r'\$\{.*\}'],
        'json': [r'\.json\b', r'\{.*".*":', r'JSON'],
        'yaml': [r'\.ya?ml\b', r'---\s*$', r'^\s*\w+:\s*$'],
        'markdown': [r'\.md\b', r'##?\s+', r'\[.*\]\(.*\)']
    }

    for lang, patterns in language_patterns.items():
        if any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE) for pattern in patterns):
            languages.append(lang)

    return languages if languages else ['general']

def detect_project_status(content: str) -> str:
    """プロジェクトの状況を検出"""
    content_lower = content.lower()

    if any(word in content_lower for word in ['完了', 'completed', 'finished', 'done']):
        return 'completed'
    elif any(word in content_lower for word in ['進行中', 'in progress', 'working on']):
        return 'in-progress'
    elif any(word in content_lower for word in ['開始', 'started', 'beginning']):
        return 'started'
    elif any(word in content_lower for word in ['計画', 'planning', 'design']):
        return 'planning'
    else:
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
    if any(word in content_lower for word in ["implement", "実装", "作成", "build"]):
        tags.append("task:implementation")
    elif any(word in content_lower for word in ["debug", "デバッグ", "修正", "fix", "error"]):
        tags.append("task:debugging")
    elif any(word in content_lower for word in ["analyze", "分析", "調査", "review"]):
        tags.append("task:analysis")
    elif any(word in content_lower for word in ["test", "テスト", "検証"]):
        tags.append("task:testing")
    elif any(word in content_lower for word in ["design", "設計", "architecture"]):
        tags.append("task:design")

    # 優先度検出
    if any(word in content_lower for word in ["urgent", "critical", "important", "緊急", "重要"]):
        tags.append("priority:high")
    elif any(word in content_lower for word in ["later", "後で", "低優先"]):
        tags.append("priority:low")
    else:
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
        timestamp = datetime.now().isoformat()
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
以下のauto-compact直前の会話内容から、次のセッションで継続作業するために必要な情報を抽出・要約して記憶してください。

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

        # TODO: 実際のMCP通信実装
        # cipher_client = MCPClient()
        # result = cipher_client.extract_and_operate_memory(
        #     interaction=memory_content,
        #     memoryMetadata=metadata
        # )

        # 現在はシミュレーション
        logger.info("Enhanced Cipher memory save simulated successfully")
        return True

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