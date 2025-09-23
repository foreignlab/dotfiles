#!/usr/bin/env python3
"""
共通ユーティリティ関数
Claude Code Cipher統合フック用の共通機能
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# 定数定義
DEFAULT_MESSAGE_LIMIT = 20  # 会話内容抽出時のデフォルトメッセージ数
CIPHER_TIMEOUT_SECONDS = 180  # Cipher通信タイムアウト（3分）
MAX_LOG_PREVIEW_LENGTH = 300  # ログプレビューの最大文字数

# Claude CLI設定
CLAUDE_CLI_COMMAND = [
    "claude",
    "--print",
    "--dangerously-skip-permissions"
]

def setup_logging(script_name: str) -> logging.Logger:
    """共通のログ設定"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'cipher_hook.log')

    # ログフォーマットにスクリプト名を含める
    log_format = f'[%(asctime)s] %(levelname)s: {script_name}: %(message)s'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

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
        logger = logging.getLogger(__name__)
        logger.error(f"Error extracting project context: {e}")
        return {"name": "unknown", "path": "unknown", "transcript_path": transcript_path}

def truncate_for_log(text: str, max_length: int = MAX_LOG_PREVIEW_LENGTH) -> str:
    """ログ用にテキストを安全に切り詰める"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_current_timestamp() -> str:
    """現在のタイムスタンプを取得"""
    return datetime.now().isoformat()