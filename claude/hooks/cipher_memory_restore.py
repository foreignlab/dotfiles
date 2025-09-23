#!/usr/bin/env python3
"""
SessionStart compact時にCipherからメモリを復元するPythonスクリプト
SessionStart Input JSONを解析し、Cipherから関連メモリを検索・復元する
"""

import json
import sys
import os
import logging
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 共通設定とユーティリティをインポート
from config import CIPHER_CONFIG, MESSAGE_CONFIG
from utils import setup_logging, extract_project_context, truncate_for_log

# ログ設定
logger = setup_logging('RESTORE')

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

# extract_project_context は shared_utils から使用

def search_cipher_memory(session_id: str, project_context: Dict[str, Any]) -> Dict[str, Any]:
    """Cipherから関連メモリを検索（現在はシミュレーション）"""
    try:
        project_name = project_context.get('name', 'unknown')

        # 検索クエリを優先度順に構築
        search_queries = []

        # 1. 直前のセッションのauto-compactメモリ
        if session_id and session_id != 'unknown':
            search_queries.append(f"session-id:{session_id[:8]} auto-compact")

        # 2. 同一プロジェクトの進行中タスク
        if project_name != 'unknown':
            search_queries.append(f"project:{project_name} status:in-progress")
            search_queries.append(f"project:{project_name} priority:high")

        # 3. 最近の高優先度タスク
        search_queries.append("auto-compact priority:high")
        search_queries.append("status:in-progress recent")

        logger.info(f"Searching Cipher with queries: {search_queries}")

        # Claude CLI経由でCipherメモリ検索
        try:
            logger.info("🔍 Attempting real Cipher memory search via Claude CLI...")

            # 最も優先度の高いクエリでCipherを検索
            found_memory = False
            cipher_response = ""

            for i, query in enumerate(search_queries[:2]):  # 上位2つのクエリを試行
                logger.info(f"🔎 Query {i+1}: {query}")

                # Cipher検索プロンプト（cipher_memory_search + ask_cipher指示）
                search_prompt = f"""以下の手順で記憶を復元してください：

1. `cipher_memory_search` を使って検索してください：
   - クエリ: "{query}"
   - プロジェクト: {project_name}
   - セッション: {session_id[:8] if session_id else 'unknown'}

2. 関連記憶が見つかったら `ask_cipher` を使って詳細を取得してください

3. 以下の情報を整理して返してください：
   - 🎯 継続中のタスク・目標
   - 🔧 技術的コンテキスト
   - 📝 重要な決定事項・発見

見つからない場合は「関連記憶なし」と返してください。"""

                # Claude CLI実行
                result = subprocess.run(
                    CIPHER_CONFIG['claude_cli_command'],
                    input=search_prompt,
                    capture_output=True,
                    text=True,
                    timeout=CIPHER_CONFIG['timeout_seconds']
                )

                if result.returncode == 0 and result.stdout.strip():
                    logger.info(f"✅ Found memories with query: {query}")
                    cipher_response = result.stdout.strip()
                    found_memory = True
                    break
                else:
                    logger.warning(f"❌ Search failed for query: {query} (return_code: {result.returncode})")

            if found_memory:
                logger.info("🎯 Real Cipher memory search successful")
                # Cipherからの実際のレスポンスを記録
                response_preview = truncate_for_log(cipher_response)
                logger.info(f"🔍 Cipher response: {response_preview}")
            else:
                logger.info("📭 No relevant memories found in Cipher")

        except Exception as e:
            logger.error(f"Real Cipher search failed: {e}")
            logger.info("🔄 Falling back to simulation")
            found_memory = False
            cipher_response = ""

        # 実際の検索結果またはフォールバック
        if found_memory and cipher_response:
            # 実際のCipher検索結果を活用
            memory_data = {
                "found": True,
                "source_session": session_id[:8] if session_id else "unknown",
                "project": project_name,
                "summary": "Cipher memory search successful",
                "cipher_response": cipher_response,
                "search_queries": search_queries[:2],
                "tags": ["cipher-restored", "auto-compact", f"project:{project_name}"],
                "last_updated": datetime.now().isoformat()
            }
            logger.info("Real Cipher memory retrieval successful")
        else:
            # フォールバックまたは検索結果なしの場合
            memory_data = {
                "found": False,
                "source_session": session_id[:8] if session_id else "unknown",
                "project": project_name,
                "summary": "No previous context found in Cipher memory",
                "search_queries": search_queries[:2],
                "last_updated": datetime.now().isoformat()
            }
            logger.info("No relevant memories found in Cipher")

        return memory_data

    except Exception as e:
        logger.error(f"Error searching Cipher memory: {e}")
        return {"found": False, "error": str(e)}

def format_restored_context(memory_data: Dict[str, Any]) -> str:
    """復元されたメモリを整形して出力"""
    try:
        if not memory_data.get("found"):
            return "🔍 No previous context found in Cipher memory."

        output_lines = [
            "🔄 CONTEXT RESTORED FROM CIPHER MEMORY",
            "",
            "📋 Previous Session Summary:",
            f"- Session: {memory_data.get('source_session', 'unknown')}",
            f"- Project: {memory_data.get('project', 'unknown')}",
            f"- Last Updated: {memory_data.get('last_updated', 'unknown')}",
            "",
            f"📝 Summary: {memory_data.get('summary', 'No summary available')}",
            ""
        ]

        # 実際のCipherレスポンスがある場合は表示
        if cipher_response := memory_data.get("cipher_response"):
            output_lines.extend([
                "🔍 Cipher Memory Content:",
                cipher_response,
                ""
            ])

        # 検索クエリ情報
        if search_queries := memory_data.get("search_queries"):
            output_lines.extend([
                f"🔎 Search Queries Used: {', '.join(search_queries)}",
                ""
            ])

        # アクティブな目標
        if active_goals := memory_data.get("active_goals", []):
            output_lines.append("🎯 Active Goals:")
            for goal in active_goals:
                output_lines.append(f"- {goal}")
            output_lines.append("")

        # 継続中のタスク
        if continuing_tasks := memory_data.get("continuing_tasks", []):
            output_lines.append("📋 Continuing Tasks:")
            for task in continuing_tasks:
                output_lines.append(f"- {task}")
            output_lines.append("")

        # 技術的コンテキスト
        if technical_context := memory_data.get("technical_context", []):
            output_lines.append("🔧 Technical Context:")
            for context in technical_context:
                output_lines.append(f"- {context}")
            output_lines.append("")

        # 重要な注意事項
        if important_notes := memory_data.get("important_notes", []):
            output_lines.append("⚠️ Important Notes:")
            for note in important_notes:
                output_lines.append(f"- {note}")
            output_lines.append("")

        # タグ情報
        if tags := memory_data.get("tags", []):
            output_lines.append(f"🏷️ Context Tags: {', '.join(tags)}")
            output_lines.append("")

        output_lines.append("💡 You can now continue from where you left off!")

        return "\n".join(output_lines)

    except Exception as e:
        logger.error(f"Error formatting restored context: {e}")
        return f"⚠️ Error formatting restored context: {e}"

def main():
    """メイン処理"""
    logger.info("Cipher memory restore script started")

    # 標準入力からSessionStart Input JSONを読み取り
    input_data = read_stdin_json()
    if not input_data:
        logger.error("Failed to read input JSON")
        sys.exit(0)  # SessionStartは失敗してもセッション開始を妨げない

    # sourceがcompactの場合のみ処理
    source = input_data.get('source', '')
    if source != 'compact':
        logger.info(f"Skipping processing for source: {source} (not compact)")
        sys.exit(0)

    session_id = input_data.get('session_id', 'unknown')
    transcript_path = input_data.get('transcript_path', '')

    logger.info(f"Processing SessionStart compact for session: {session_id}")

    # プロジェクトコンテキストを抽出
    project_context = extract_project_context(transcript_path)
    logger.info(f"Project context: {project_context}")

    # Cipherからメモリを検索
    memory_data = search_cipher_memory(session_id, project_context)

    # 復元されたコンテキストを整形して出力
    restored_context = format_restored_context(memory_data)

    # 標準出力に復元されたコンテキストを出力
    print(restored_context)

    if memory_data.get("found"):
        logger.info("Successfully restored context from Cipher")
    else:
        logger.info("No context found to restore")

    sys.exit(0)

if __name__ == "__main__":
    main()