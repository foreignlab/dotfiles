#!/usr/bin/env bash
# tmux-launch — fzf-driven tmux session picker.
# 既存セッションへアタッチ / 新規作成 / そのまま素のシェル(Esc) を選ばせる。
# .zshrc から「対話的かつ tmux 外」のときに呼ばれる想定（Mac/WSL 共通）。
# 重要: 呼び出し元は exec せず「呼ぶ」だけ。Esc 時はここを exit して元のシェルへ戻る。

# tmux の中なら何もしない（入れ子防止）
[ -n "${TMUX:-}" ] && exit 0
# tmux が無ければ何もせず素のシェルのまま（呼び出し元へ戻る）
command -v tmux >/dev/null 2>&1 || exit 0

# fzf が無い環境では従来どおり attach-or-new にフォールバック
if ! command -v fzf >/dev/null 2>&1; then
  tmux attach 2>/dev/null && exit 0
  exec tmux new -s main
fi

new_entry='＋ new session'
sessions="$(tmux list-sessions -F '#S' 2>/dev/null)"

choice="$(
  {
    [ -n "$sessions" ] && printf '%s\n' "$sessions"
    printf '%s\n' "$new_entry"
  } | fzf --prompt='tmux ❯ ' --reverse --height='40%' \
          --header='Enter: アタッチ / ＋ new session: 新規 / Esc: tmuxを使わず素のシェルへ'
)"

# Esc / 未選択 → 何もせず呼び出し元の素のシェルへ戻る
[ -z "$choice" ] && exit 0

if [ "$choice" = "$new_entry" ]; then
  printf 'new session name (空欄で自動命名): '
  read -r name
  [ -n "$name" ] && exec tmux new -s "$name"
  exec tmux new
fi

exec tmux attach -t "$choice"
