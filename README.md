# dotfiles

[![macOS](https://img.shields.io/badge/macOS-supported-green.svg)](https://www.apple.com/macos/)

Personal dotfiles collection for macOS development environment setup. This repository contains carefully configured shell, git, and terminal multiplexer settings optimized for productivity.

## Features

- **Zsh Configuration**: Enhanced shell with plugins, custom functions, and Powerlevel10k theme
- **Git Setup**: User configuration and global ignore patterns
- **Tmux Configuration**: Terminal multiplexer with plugins and custom key bindings
- **FZF Integration**: Fuzzy finder with custom preview options
- **Automated Installation**: One-command setup with organized directory structure

## Quick Start

```bash
git clone https://github.com/foreignlab/dotfiles.git
cd dotfiles
./install.sh
```

**Prerequisites**: macOS with Zsh as the default shell

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/foreignlab/dotfiles.git
cd dotfiles
```

### 2. Install Zap Plugin Manager (Required)
```bash
curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh | zsh
```

### 3. Run the Installer
```bash
./install.sh
```

The installer checks for required dependencies and creates symlinks from the organized directory structure to your home directory.

### 4. Restart Your Shell
```bash
exec zsh
# or open a new terminal session
```

## What's Included

### Zsh Configuration (`zsh/`)
- **Plugin Management**: Zap plugin manager
- **Theme**: Powerlevel10k with custom configuration
- **Plugins**: autosuggestions, completions, syntax highlighting
- **Custom Functions**: 
  - `fssh()` - FZF-powered SSH host selection
  - `gcd()` - Navigate to ghq repositories with FZF
  - `fcd()` - FZF directory navigation
  - `ff()` - FZF file finder with editor selection
- **Aliases**: Enhanced `ls`, `cat`, and `diff` commands using modern tools

### Git Configuration (`git/`)
- User configuration with email and name
- Git tools integration (Sourcetree, diff tools)
- Global ignore patterns for common development files

### Tmux Configuration (`tmux/`)
- **Plugin Manager**: TPM (Tmux Plugin Manager)
- **Plugins**: tmux-resurrect, tmux-continuum, tmux-fzf
- **Features**: Session persistence, FZF integration for session/window/pane switching
- **Custom Key Bindings**: Intuitive pane splitting and navigation

## Dependencies

These tools are referenced in the configurations and should be installed:

```bash
# Essential tools
brew install zsh tmux git fzf fd bat eza delta

# Development tools (optional)
brew install volta pyenv jenv direnv ghq gh

# For Powerlevel10k
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# Plugin managers will be installed automatically:
# - Zap (Zsh plugin manager)
# - TPM (Tmux plugin manager)
```

## Directory Structure

```
dotfiles/
├── install.sh              # Automated installation script
├── zsh/                     # Zsh shell configuration
│   ├── .zshrc               # Main configuration with plugins and functions
│   ├── .zprofile            # Profile loaded at login
│   ├── .p10k.zsh            # Powerlevel10k prompt configuration
│   └── .fzf.zsh             # FZF configuration and key bindings
├── git/                     # Git version control configuration
│   ├── .gitconfig           # User configuration and tools
│   └── .gitignore_global    # Global ignore patterns
└── tmux/                    # Tmux terminal multiplexer configuration
    └── .tmux.conf           # Configuration with plugins and key bindings
```

## Customization

### Personal Git Configuration
Edit `git/.gitconfig` to update your name and email:
```ini
[user]
    name = Your Name
    email = your.email@example.com
```

### Zsh Customization
- Modify `zsh/.zshrc` for aliases and functions
- Update `zsh/.p10k.zsh` for prompt customization
- Add environment variables to `zsh/.zprofile`

### Tmux Customization
- Edit `tmux/.tmux.conf` for key bindings and settings
- Plugin configuration is managed through TPM

## Updating

To update your dotfiles:
```bash
cd dotfiles
git pull
./install.sh
```
