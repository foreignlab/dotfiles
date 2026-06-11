#!/bin/bash

# Dotfiles installer for macOS
# Simple symlink creation script

DOTFILES_DIR="$PWD"

echo "Installing dotfiles..."

# Check for Zap plugin manager
if [ ! -f "$HOME/.local/share/zap/zap.zsh" ]; then
  echo ""
  echo "⚠️  Warning: Zap plugin manager not found."
  echo "Zsh configuration requires Zap to function properly."
  echo ""
  echo "Please install Zap first:"
  echo "  curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh | zsh"
  echo ""
  echo "Then run this installer again."
  exit 1
fi

# Tmux Plugin Manager (TPM)
# これが無いと .tmux.conf の @plugin（dracula 等）が一切読み込まれない
if [ ! -d "$HOME/.tmux/plugins/tpm" ]; then
  echo "Installing TPM (tmux plugin manager)..."
  git clone https://github.com/tmux-plugins/tpm "$HOME/.tmux/plugins/tpm"
fi

# Zsh configuration
ln -sf "$DOTFILES_DIR/zsh/.zshrc" "$HOME/.zshrc"
ln -sf "$DOTFILES_DIR/zsh/.zprofile" "$HOME/.zprofile"
ln -sf "$DOTFILES_DIR/zsh/.p10k.zsh" "$HOME/.p10k.zsh"
ln -sf "$DOTFILES_DIR/zsh/.fzf.zsh" "$HOME/.fzf.zsh"

# Git configuration
ln -sf "$DOTFILES_DIR/git/.gitconfig" "$HOME/.gitconfig"
ln -sf "$DOTFILES_DIR/git/.gitignore_global" "$HOME/.gitignore_global"

# Tmux configuration
ln -sf "$DOTFILES_DIR/tmux/.tmux.conf" "$HOME/.tmux.conf"

# Neovim configuration (link the whole directory; lazy.nvim bootstraps itself on first launch)
mkdir -p "$HOME/.config"
ln -snf "$DOTFILES_DIR/nvim" "$HOME/.config/nvim"

# Install tmux plugins non-interactively (TPM must be present)
if [ -x "$HOME/.tmux/plugins/tpm/bin/install_plugins" ]; then
  echo "Installing tmux plugins..."
  "$HOME/.tmux/plugins/tpm/bin/install_plugins" >/dev/null 2>&1 || true
fi

echo "Dotfiles installed successfully!"
echo "Note: You may need to restart your shell or run 'source ~/.zshrc' to apply changes."