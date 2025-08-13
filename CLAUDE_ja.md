# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリでコードを扱う際のガイダンスを提供します。

## リポジトリ概要
これは、シェル設定と開発環境のセットアップファイルを含む個人のdotfilesリポジトリです。このリポジトリは以下の設定ファイルを管理しています：
- Zshシェル (.zshrc, .zprofile, .p10k.zsh)
- Tmuxターミナルマルチプレクサ (.tmux.conf)
- Gitバージョン管理 (.gitconfig, .gitignore_global)
- FZFファジーファインダー (.fzf.zsh)

## ファイル構造
このリポジトリは論理的なディレクトリで設定ファイルが整理されています：

```
dotfiles/
├── install.sh              # 自動インストールスクリプト
├── zsh/                     # Zshシェル設定
│   ├── .zshrc               # プラグイン、エイリアス、カスタム関数を含むメインのzsh設定
│   ├── .zprofile            # ログイン時に読み込まれるZshプロファイル
│   ├── .p10k.zsh            # Powerlevel10kプロンプト設定
│   └── .fzf.zsh             # FZF設定とキーバインディング
├── git/                     # Gitバージョン管理設定
│   ├── .gitconfig           # Gitユーザー設定とツール設定
│   └── .gitignore_global    # グローバルGit無視パターン
└── tmux/                    # Tmuxターミナルマルチプレクサ設定
    └── .tmux.conf           # プラグインとキーバインディングを含むTmux設定
```

## 主要な設定コンポーネント

### Zsh設定
zsh設定では以下を使用しています：
- Zapプラグインマネージャーによるzshプラグイン管理
- プロンプトテーマのPowerlevel10k
- カスタムプレビューオプション付きファジーファインダーのFZF
- ナビゲーション強化のためのカスタム関数：`fssh()`, `gcd()`, `fcd()`, `ff()`

### Tmux設定
Tmux設定には以下が含まれます：
- TPM（Tmux Plugin Manager）によるプラグイン管理
- tmux-resurrectとtmux-continuumによるセッション永続化
- セッション/ウィンドウ/ペイン切り替えのためのFZF統合
- ペイン分割のためのカスタムキーバインディング

### 開発ツール統合
設定では以下の開発ツールを統合しています：
- Node.jsバージョン管理のVolta
- Pythonバージョン管理のPyenv
- Javaバージョン管理のJenv
- 環境変数管理のDirenv
- リポジトリ管理のghq

## インストール/セットアップ
このdotfilesリポジトリには自動インストールスクリプトが含まれています：

1. リポジトリをクローン: `git clone https://github.com/foreignlab/dotfiles.git`
2. ディレクトリに移動: `cd dotfiles`
3. インストーラーを実行: `./install.sh`

install.shスクリプトは、整理されたディレクトリ構造からユーザーのホームディレクトリの適切な場所に自動的にシンボリックリンクを作成します。

## よく使うコマンド
- `./install.sh` - シンボリックリンクによるすべてのdotfilesのインストール
- `git pull && ./install.sh` - dotfilesの更新と再インストール

この設定専用リポジトリには、ビルド、テスト、またはリントコマンドは適用されません。