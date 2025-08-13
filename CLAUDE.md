# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This is a personal dotfiles repository containing shell configuration and development environment setup files. The repository manages configuration files for:
- Zsh shell (.zshrc, .zprofile, .p10k.zsh)
- Tmux terminal multiplexer (.tmux.conf)
- Git version control (.gitconfig, .gitignore_global)
- FZF fuzzy finder (.fzf.zsh)

## File Structure
The repository is organized into logical directories with configuration files:

```
dotfiles/
├── install.sh              # Automated installation script
├── zsh/                     # Zsh shell configuration
│   ├── .zshrc               # Main zsh configuration with plugins, aliases, and custom functions
│   ├── .zprofile            # Zsh profile loaded at login
│   ├── .p10k.zsh            # Powerlevel10k prompt configuration
│   └── .fzf.zsh             # FZF configuration and key bindings
├── git/                     # Git version control configuration
│   ├── .gitconfig           # Git user configuration and tools setup
│   └── .gitignore_global    # Global Git ignore patterns
└── tmux/                    # Tmux terminal multiplexer configuration
    └── .tmux.conf           # Tmux configuration with plugins and key bindings
```

## Key Configuration Components

### Zsh Setup
The zsh configuration uses:
- Zap plugin manager for managing zsh plugins
- Powerlevel10k for the prompt theme
- FZF for fuzzy finding with custom preview options
- Custom functions: `fssh()`, `gcd()`, `fcd()`, `ff()` for enhanced navigation

### Tmux Configuration
Tmux setup includes:
- Plugins managed by TPM (Tmux Plugin Manager)
- Session persistence with tmux-resurrect and tmux-continuum
- FZF integration for session/window/pane switching
- Custom key bindings for pane splitting

### Development Tools Integration
The configuration integrates several development tools:
- Volta for Node.js version management
- Pyenv for Python version management
- Jenv for Java version management
- Direnv for environment variable management
- ghq for repository management

## Installation/Setup
This dotfiles repository includes an automated installation script:

1. Clone the repository: `git clone https://github.com/foreignlab/dotfiles.git`
2. Navigate to the directory: `cd dotfiles`
3. Run the installer: `./install.sh`

The install.sh script automatically creates symlinks from the organized directory structure to the appropriate locations in the user's home directory.

## Common Commands
- `./install.sh` - Install all dotfiles via symlinks
- `git pull && ./install.sh` - Update dotfiles and reinstall

No build, test, or lint commands are applicable for this configuration-only repository.