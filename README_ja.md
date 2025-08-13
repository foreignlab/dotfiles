# dotfiles

[![macOS](https://img.shields.io/badge/macOS-supported-green.svg)](https://www.apple.com/macos/)

macOS開発環境セットアップのための個人用dotfilesコレクション。生産性に最適化された、慎重に設定されたシェル、git、ターミナルマルチプレクサ設定が含まれています。

## 特徴

- **Zsh設定**: プラグイン、カスタム関数、Powerlevel10kテーマを備えた強化されたシェル
- **Git設定**: ユーザー設定とグローバル無視パターン
- **Tmux設定**: プラグインとカスタムキーバインディングを備えたターミナルマルチプレクサ
- **FZF統合**: カスタムプレビューオプション付きファジーファインダー
- **自動インストール**: 整理されたディレクトリ構造による1コマンドセットアップ

## クイックスタート

```bash
git clone https://github.com/foreignlab/dotfiles.git
cd dotfiles
./install.sh
```

**前提条件**: デフォルトシェルがZshのmacOS

## インストール

### 1. リポジトリをクローン
```bash
git clone https://github.com/foreignlab/dotfiles.git
cd dotfiles
```

### 2. Zapプラグインマネージャーをインストール（必須）
```bash
curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh | zsh
```

### 3. インストーラーを実行
```bash
./install.sh
```

インストーラーは必要な依存関係をチェックし、整理されたディレクトリ構造からホームディレクトリにシンボリックリンクを作成します。

### 4. シェルを再起動
```bash
exec zsh
# または新しいターミナルセッションを開く
```

## 含まれる内容

### Zsh設定 (`zsh/`)
- **プラグイン管理**: Zapプラグインマネージャー
- **テーマ**: カスタム設定のPowerlevel10k
- **プラグイン**: autosuggestions、completions、syntax highlighting
- **カスタム関数**: 
  - `fssh()` - FZFを使ったSSHホスト選択
  - `gcd()` - FZFでghqリポジトリにナビゲート
  - `fcd()` - FZFディレクトリナビゲーション
  - `ff()` - エディタ選択付きFZFファイルファインダー
- **エイリアス**: モダンツールを使用した`ls`、`cat`、`diff`コマンドの強化

### Git設定 (`git/`)
- メールと名前を含むユーザー設定
- Gitツール統合（Sourcetree、diffツール）
- 一般的な開発ファイルのグローバル無視パターン

### Tmux設定 (`tmux/`)
- **プラグインマネージャー**: TPM（Tmux Plugin Manager）
- **プラグイン**: tmux-resurrect、tmux-continuum、tmux-fzf
- **機能**: セッション永続化、セッション/ウィンドウ/ペイン切り替えのFZF統合
- **カスタムキーバインディング**: 直感的なペイン分割とナビゲーション

## 依存関係

これらのツールが設定で参照されており、インストールが必要です：

```bash
# 必須ツール
brew install zsh tmux git fzf fd bat eza delta

# 開発ツール（オプション）
brew install volta pyenv jenv direnv ghq gh

# Powerlevel10k用
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# プラグインマネージャーは自動的にインストールされます：
# - Zap（Zshプラグインマネージャー）
# - TPM（Tmuxプラグインマネージャー）
```

## ディレクトリ構造

```
dotfiles/
├── install.sh              # 自動インストールスクリプト
├── zsh/                     # Zshシェル設定
│   ├── .zshrc               # プラグインと関数を含むメイン設定
│   ├── .zprofile            # ログイン時に読み込まれるプロファイル
│   ├── .p10k.zsh            # Powerlevel10kプロンプト設定
│   └── .fzf.zsh             # FZF設定とキーバインディング
├── git/                     # Gitバージョン管理設定
│   ├── .gitconfig           # ユーザー設定とツール
│   └── .gitignore_global    # グローバル無視パターン
└── tmux/                    # Tmuxターミナルマルチプレクサ設定
    └── .tmux.conf           # プラグインとキーバインディングを含む設定
```

## カスタマイズ

### 個人Git設定
`git/.gitconfig`を編集して名前とメールを更新：
```ini
[user]
    name = Your Name
    email = your.email@example.com
```

### Zshカスタマイズ
- エイリアスと関数の変更は`zsh/.zshrc`を修正
- プロンプトのカスタマイズは`zsh/.p10k.zsh`を更新
- 環境変数の追加は`zsh/.zprofile`に

### Tmuxカスタマイズ
- キーバインディングと設定の変更は`tmux/.tmux.conf`を編集
- プラグイン設定はTPMで管理

## 更新

dotfilesを更新するには：
```bash
cd dotfiles
git pull
./install.sh
```
