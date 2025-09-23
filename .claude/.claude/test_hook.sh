#!/bin/bash

# PreCompact hookのテストスクリプト
# サンプルのPreCompact Input JSONを生成してフックをテストする

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$SCRIPT_DIR/hooks/save_to_cipher.sh"

# テスト用JSONを生成
create_test_json() {
    local trigger="$1"
    local transcript_path="$2"

    cat <<EOF
{
  "session_id": "test_session_$(date +%s)",
  "transcript_path": "$transcript_path",
  "hook_event_name": "PreCompact",
  "trigger": "$trigger",
  "custom_instructions": ""
}
EOF
}

# テスト用トランスクリプトファイルを作成
create_test_transcript() {
    local transcript_file="$1"

    cat <<'EOF' > "$transcript_file"
{"type": "text", "role": "user", "content": "こんにちは、Claude Code のテストをしています。Pythonでauto-compact フック機能を実装中です"}
{"type": "text", "role": "assistant", "content": "こんにちは！Claude Code のテストをお手伝いします。Python実装を進めましょう"}
{"type": "tool_use", "name": "Write", "content": "cipher_memory_save.py"}
{"type": "text", "role": "user", "content": "auto-compact が発動した時にCipherに記憶を保存したいです。重要な決定事項として、構造化されたプロンプトとスマートタグを使用します"}
{"type": "text", "role": "assistant", "content": "auto-compact 時のCipherへの記憶保存機能を実装しましょう。プロジェクトの状況は進行中です"}
{"type": "tool_use", "name": "TodoWrite", "content": "タスク管理"}
{"type": "text", "role": "user", "content": "次のセッションでこの内容を思い出せるように、プロジェクトコンテキストとタグ機能を追加してください"}
EOF
}

# テスト実行
run_test() {
    local test_name="$1"
    local trigger="$2"

    echo "=== $test_name ==="

    # テスト用トランスクリプトファイルを作成
    local transcript_file="/tmp/test_transcript_$$.jsonl"
    create_test_transcript "$transcript_file"

    # テスト用JSONを生成
    local test_json
    test_json=$(create_test_json "$trigger" "$transcript_file")

    echo "Input JSON:"
    echo "$test_json" | jq .

    echo ""
    echo "Running hook..."

    # フックを実行
    if echo "$test_json" | "$HOOK_SCRIPT"; then
        echo "✅ Hook executed successfully"
    else
        echo "❌ Hook execution failed"
    fi

    # テスト用ファイルをクリーンアップ
    rm -f "$transcript_file"

    echo ""
}

# メイン実行
main() {
    echo "Claude Code PreCompact Hook Test"
    echo "=================================="
    echo ""

    # フックスクリプトが存在することを確認
    if [[ ! -f "$HOOK_SCRIPT" ]]; then
        echo "❌ Hook script not found: $HOOK_SCRIPT"
        exit 1
    fi

    # jqコマンドの存在確認
    if ! command -v jq >/dev/null 2>&1; then
        echo "⚠️ jq not found. JSON will not be prettified."
        echo ""
    fi

    # テストケース1: auto trigger（処理される）
    run_test "Test 1: Auto Trigger" "auto"

    # テストケース2: manual trigger（スキップされる）
    run_test "Test 2: Manual Trigger (should be skipped)" "manual"

    echo "=== Log Output ==="
    local log_file="$SCRIPT_DIR/hooks/logs/cipher_hook.log"
    if [[ -f "$log_file" ]]; then
        echo "Last 10 lines of log:"
        tail -10 "$log_file"
    else
        echo "No log file found at $log_file"
    fi

    echo ""
    echo "Test completed!"
}

main "$@"