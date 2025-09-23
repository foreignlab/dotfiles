#!/usr/bin/env python3
"""
設定ファイル
Claude Code Cipher統合フック用の設定項目
"""

# Cipher通信設定
CIPHER_CONFIG = {
    "timeout_seconds": 180,  # 3分
    "max_retries": 1,
    "claude_cli_command": [
        "claude",
        "--print",
        "--dangerously-skip-permissions"
    ]
}

# メッセージ処理設定
MESSAGE_CONFIG = {
    "default_limit": 20,  # 抽出するメッセージ数のデフォルト
    "max_preview_length": 300,  # ログプレビューの最大文字数
    "max_response_length": 200  # Cipherレスポンスプレビューの最大文字数
}

# プロジェクト検出設定
PROJECT_CONFIG = {
    "search_directories": ['Documents', 'Projects', 'workspace', 'code'],
    "default_project_name": "unknown",
    "default_working_dir": "unknown"
}

# ログ設定
LOG_CONFIG = {
    "level": "INFO",
    "log_dir": "logs",
    "log_file": "cipher_hook.log",
    "encoding": "utf-8"
}

# 言語検出パターン
LANGUAGE_PATTERNS = {
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

# タスク検出パターン
TASK_PATTERNS = {
    'implementation': ["implement", "実装", "作成", "build"],
    'debugging': ["debug", "デバッグ", "修正", "fix", "error"],
    'analysis': ["analyze", "分析", "調査", "review"],
    'testing': ["test", "テスト", "検証"],
    'design': ["design", "設計", "architecture"]
}

# 優先度検出パターン
PRIORITY_PATTERNS = {
    'high': ["urgent", "critical", "important", "緊急", "重要"],
    'low': ["later", "後で", "低優先"],
    'medium': []  # デフォルト
}

# ステータス検出パターン
STATUS_PATTERNS = {
    'completed': ['完了', 'completed', 'finished', 'done'],
    'in-progress': ['進行中', 'in progress', 'working on'],
    'started': ['開始', 'started', 'beginning'],
    'planning': ['計画', 'planning', 'design'],
    'active': []  # デフォルト
}