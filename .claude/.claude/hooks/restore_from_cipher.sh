#!/bin/bash

# SessionStart compact時にCipherからメモリを復元するフック
# SessionStart Inputイベントで呼び出される

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/cipher_hook.log"
PYTHON_SCRIPT="$SCRIPT_DIR/cipher_memory_restore.py"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] RESTORE: $1" >> "$LOG_FILE"
}

# メイン処理
main() {
    log "SessionStart compact hook started"

    # stdinからJSONを読み取り
    input_json=$(cat)

    # JSONが空でないことを確認
    if [[ -z "$input_json" ]]; then
        log "ERROR: No input received from stdin"
        exit 1
    fi

    log "SessionStart input JSON received: $input_json"

    # Pythonスクリプトが存在することを確認
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        log "ERROR: Python restore script not found at $PYTHON_SCRIPT"
        exit 1
    fi

    # Pythonスクリプトを実行してCipherからメモリを復元
    if echo "$input_json" | python3 "$PYTHON_SCRIPT"; then
        log "Python restore script executed successfully"
        exit 0
    else
        log "ERROR: Python restore script failed with exit code $?"
        # SessionStartフックは失敗してもセッション開始を妨げない
        exit 0
    fi
}

# エラーハンドリング
trap 'log "ERROR: Unexpected error occurred at line $LINENO"' ERR

# スクリプト実行
main "$@"