# Homebrew（存在する場所を自動検出して shellenv を読み込む。Apple Silicon / Intel Mac / Linuxbrew 対応）
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
elif [ -x /home/linuxbrew/.linuxbrew/bin/brew ]; then
  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
fi

# Obsidian アプリの CLI パス（macOS のみ存在）
if [ -d "/Applications/Obsidian.app/Contents/MacOS" ]; then
  export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
fi
