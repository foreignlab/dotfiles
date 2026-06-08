###
### 基本設定
###
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export TERM="xterm-256color"
#export EDITOR=vim

###
### ヒストリー・履歴設定
###
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000
setopt EXTENDED_HISTORY       # 日付付きで履歴保存
setopt INC_APPEND_HISTORY     # コマンド実行ごとに履歴追記
setopt HIST_IGNORE_ALL_DUPS   # 重複履歴はすべて無視
setopt SHARE_HISTORY          # 複数シェルで履歴共有
setopt HIST_IGNORE_SPACE      # 先頭スペースコマンドは履歴に残さない

###
### 補完・インタラクション
###
autoload -Uz compinit && compinit -u
zstyle ':completion:*' menu select
zstyle ':completion:*:descriptions' format '%B%d%b'     # 補完候補の説明を太字
setopt COMPLETE_IN_WORD       # カーソル位置で補完
setopt AUTO_CD                # ディレクトリ名だけでcd
setopt AUTO_PUSHD             # cdの履歴自動記録（cd -[Tab]で移動）
setopt INTERACTIVE_COMMENTS   # #でコメントOK
setopt NO_BEEP                # ビープ音なし
setopt CORRECT                # コマンドtypo時に候補を出す

###
### zap プラグインマネージャの読み込み
###
if [ -f "$HOME/.local/share/zap/zap.zsh" ]; then
  source "$HOME/.local/share/zap/zap.zsh"
fi

plug "zsh-users/zsh-autosuggestions"
plug "zsh-users/zsh-completions"
plug "zsh-users/zsh-syntax-highlighting"
plug "romkatv/powerlevel10k"

###
### fzf
###
#-- fzfの表示オプション
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'

#-- Ctrl-TやCtrl-Rなどfzfで表示するときのプレビューに色を付ける例
export FZF_CTRL_T_OPTS="--preview 'bat --style=numbers --color=always {} | head -100'"
export FZF_ALT_C_OPTS="--preview 'eza -T {} | head -40'"

#-- Ctrl-Tで候補一覧を出す際、fd（超高速ファイル検索）を使う例
export FZF_CTRL_T_COMMAND='fd --type f --hidden --follow --exclude .git'

#-- Ctrl-Rで履歴検索する時のプレビュー
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window down:3:wrap"

#-- fzf拡張スクリプトの読み込み
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# fzf-tmuxでポップアップ表示（幅80%、高さ60%）
export FZF_TMUX=1
export FZF_TMUX_OPTS="-p 80%,60%"

###
### Powerlevel10k の読み込み
###  Obsidian 内蔵ターミナル（$OBSIDIAN_TERMINAL）では競合するため無効化する
###
if [[ -z "$OBSIDIAN_TERMINAL" ]]; then
  # Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
  # Initialization code that may require console input (password prompts, [y/n]
  # confirmations, etc.) must go above this block; everything else may go below.
  if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
  fi

  [[ -r "${HOME}/.p10k.zsh" ]] && source "${HOME}/.p10k.zsh"
fi

###
### エイリアス
###
alias ll='eza -l --octal-permissions'
alias la='eza -la --octal-permissions'
alias lt='eza -l --octal-permissions --sort newest -r'
alias ltr='eza -l --octal-permissions --sort newest'
alias lat='eza -la --octal-permissions --sort newest -r'
alias latr='eza -la --octal-permissions --sort newest'
# Debian/Ubuntu(WSL) では bat が batcat という名前で入るため、その場合だけ別名を張る
if command -v batcat >/dev/null 2>&1; then
  alias bat='batcat'
fi
alias cat='bat --style=plain'
alias diff='delta'
alias vim='nvim'
alias vi='nvim'
alias view='nvim -R'
alias ocd='cd $HOME/Documents/Obsidian/Notes'
alias cc='claude'
alias ccw='CLAUDE_CONFIG_DIR=$HOME/.claude-work claude'
# alias ccw='CLAUDE_CONFIG_DIR=$HOME/.claude-work \
#     CLAUDE_CODE_USE_VERTEX=1 \
#     CLOUD_ML_REGION=us-east5 \
#     ANTHROPIC_VERTEX_PROJECT_ID=prod-mcc-ai-sonoda-dais \
#     ANTHROPIC_MODEL="claude-sonnet-4-5@20250929" \
#     ANTHROPIC_SMALL_FAST_MODEL="claude-haiku-4-5@20251001" \
#     claude --verbose'
alias gh-p='gh auth switch --user foreignlab >/dev/null 2>&1 && gh'
alias gh-w='gh auth switch --user sonoda-daisuke >/dev/null 2>&1 && gh'

###
### PATH
###
#-- ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

#-- Node.js などのバージョン管理
#   mise があればそれを使い（主に macOS）、無ければ nvm にフォールバック（主に WSL）。
#   両方入っていても mise 優先で衝突しない。
if command -v mise >/dev/null 2>&1; then
  eval "$(mise activate zsh)"
elif [ -s "$HOME/.nvm/nvm.sh" ]; then
  export NVM_DIR="$HOME/.nvm"
  source "$NVM_DIR/nvm.sh"
  [ -s "$NVM_DIR/bash_completion" ] && source "$NVM_DIR/bash_completion"
fi

# #-- pyenv（Python のバージョン管理）
# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init - zsh)"

#-- direnv
eval "$(direnv hook zsh)"

# #-- jenv（Java バージョン管理）
# export JENV_ROOT="$HOME/.jenv"
# export PATH="$JENV_ROOT/bin:$PATH"
# eval "$(jenv init -)"

# export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

#-- Go
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"

###
### 自作関数
###
#-- _fzf(): fzfを実行する環境に合わせて適切なfzfコマンドを選択
function _fzf() {
  if [ -n "$TMUX" ] && command -v fzf-tmux >/dev/null 2>&1; then
    fzf-tmux "$@"
  else
    fzf "$@"
  fi
}

#-- fssh(): fzfでssh先を選べる
function fssh() {
  local sshLoginHost
  sshLoginHost=$(awk '/^Host /{print $2}' ~/.ssh/config | _fzf)
  [ -z "$sshLoginHost" ] && return 1
  ssh "$sshLoginHost"
}

#-- gcd(): ghqでクローンしてきたリポジトリにfzfで移動できる
function gcd() {
  local repo
  repo=$(ghq list | _fzf)
  [ -z "$repo" ] && return 1
  cd "$(ghq root)/$repo" || return

  if [[ -n "$TMUX" ]]; then
    tmux rename-session -t "$(basename "$repo")"
  fi
}

#-- fcd(): fzfでcd先を選べる
function fcd() {
  local dir
  dir=$(fd --type d --color=always | _fzf --ansi --preview 'eza -T {} | head -40')
  [[ -n "$dir" ]] && cd "$dir"
}

#-- ff(): fzfでfileをfindして、既定のeditorで開く
function ff() {
  local file editor
  file=$(fd --type f | _fzf --ansi --preview 'bat --style=numbers --color=always {} | head -100')
  [[ -z "$file" ]] && return

  editor=$(printf "nvim\nvim\ncode\nless\ncat\nopen" | _fzf --prompt="Editor? " --height=6)
  [[ -z "$editor" ]] && return

  case "$editor" in
    code)
      code "$file"
      ;;
    open)
      open "$file"
      ;;
    *)
      "$editor" "$file"
      ;;
  esac
}

# function check_claude() {
#   local current_version
#   local latest_version

#   echo "🔍 Checking for Claude Code updates..."

#   if ! command -v claude &> /dev/null; then
#     echo "❌ Claude Code is not installed. Please install it first."
#     echo "💡 `npm install -g @anthropic-ai/claude-code`"
#     return 1
#   fi

#   current_version=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
#   if [ -z "$current_version" ]; then
#     echo "❌ Could not determine current version. Please check if Claude Code is installed correctly."
#     return 1
#   fi
#   echo "📦 Current version: $current_version"

#   latest_version=$(npm view @anthropic-ai/claude-code version 2>/dev/null | tr -d '\n')
#   if [ -z "$latest_version" ]; then
#     echo "❌ Could not fetch latest version from npm."
#     return 1
#   fi
#   echo "🆕 Latest version: $latest_version"

#   if [[ "$current_version" == "$latest_version" ]]; then
#     echo "✅ Claude Code is up to date."
#     return 0
#   fi

#   echo "🔄 New version available: $current_version -> $latest_version"
#   echo "🔄 Updating Claude Code..."

#   if npm update -g @anthropic-ai/claude-code; then
#     local new_version
#     new_version=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
#     echo "✅ Successfully updated to version: $new_version"
#     return 0
#   else
#     echo "❌ Failed to update Claude Code."
#     echo "💡 `npm update -g @anthropic-ai/claude-code`"
#     return 1
#   fi
# }

### For ForeignLab.AI Settings
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=foreignlab123
export SPARK_JARS_HOME="$HOME/spark-jars"
export SPARK_S3A_JARS="$SPARK_JARS_HOME/hadoop-aws-3.3.4.jar,$SPARK_JARS_HOME/aws-java-sdk-bundle-1.12.262.jar"

### For Gemini CLI
export GOOGLE_GENAI_USE_GCA=true

# Added by LM Studio CLI (lms)
export PATH="$PATH:$HOME/.lmstudio/bin"
# End of LM Studio CLI section
autoload -U +X bashcompinit && bashcompinit
# mc (MinIO Client) のシェル補完 — インストール済みのときのみ
if command -v mc >/dev/null 2>&1; then
  complete -o nospace -C "$(command -v mc)" mc
fi

# # Added by Antigravity
# export PATH="$HOME/.antigravity/antigravity/bin:$PATH"

# bun completions（$HOME 展開で Mac(/Users) と WSL(/home) 両対応）
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

alias claude-mem='bun "$HOME/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-service.cjs"'

# Google Cloud SDK（存在する場合のみ読み込む。$HOME 展開で Mac/WSL 両対応）
if [ -f "$HOME/Downloads/google-cloud-sdk/path.zsh.inc" ]; then . "$HOME/Downloads/google-cloud-sdk/path.zsh.inc"; fi

# gcloud のシェルコマンド補完
if [ -f "$HOME/Downloads/google-cloud-sdk/completion.zsh.inc" ]; then . "$HOME/Downloads/google-cloud-sdk/completion.zsh.inc"; fi

#if [ -z "$TMUX" ] && [ -n "$PS1" ]; then
#  tmux attach || tmux
#fi
fastfetch
