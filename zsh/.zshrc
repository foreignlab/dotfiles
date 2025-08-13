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
###
[[ -r "${HOME}/.p10k.zsh" ]] && source "${HOME}/.p10k.zsh"

###
### エイリアス
###
alias ll='eza -l --octal-permissions'
alias la='eza -la --octal-permissions'
alias lt='eza -l --octal-permissions --sort newest -r'
alias ltr='eza -l --octal-permissions --sort newest'
alias lat='eza -la --octal-permissions --sort newest -r'
alias latr='eza -la --octal-permissions --sort newest'
alias cat='bat --style=plain'
alias diff='delta'
#alias vim='nvim'
#alias vi='nvim'

###
### PATH
###
#-- 0. ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

#-- 1. Volta（Node.js のバージョン管理）
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"

#-- 2. pyenv（Python のバージョン管理）
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"

#-- 3. direnv
eval "$(direnv hook zsh)"

#-- 4. jenv（Java バージョン管理）
export JENV_ROOT="$HOME/.jenv"
export PATH="$JENV_ROOT/bin:$PATH"
eval "$(jenv init -)"

export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

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

