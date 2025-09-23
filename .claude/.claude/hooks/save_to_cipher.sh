#!/bin/bash

# Auto-Compact時にCipherにメモリを保存するフック
# PreCompact Inputイベントで呼び出される

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/cipher_hook.log"
PYTHON_SCRIPT="$SCRIPT_DIR/cipher_memory_save.py"

# ログディレクトリが存在しない場合は作成
mkdir -p "$SCRIPT_DIR/logs"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# メイン処理
main() {
    log "PreCompact hook started"

    # stdinからJSONを読み取り
    input_json=$(cat)

    # JSONが空でないことを確認
    if [[ -z "$input_json" ]]; then
        log "ERROR: No input received from stdin"
        exit 1
    fi

    log "Input JSON received: $input_json"

    # Pythonスクリプトが存在することを確認
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        log "ERROR: Python script not found at $PYTHON_SCRIPT"
        exit 1
    fi

    # Pythonスクリプトを実行
    if echo "$input_json" | python3 "$PYTHON_SCRIPT"; then
        log "Python script executed successfully"
        exit 0
    else
        log "ERROR: Python script failed with exit code $?"
        exit 1
    fi
}

# エラーハンドリング
trap 'log "ERROR: Unexpected error occurred at line $LINENO"' ERR

# スクリプト実行
main "$@"