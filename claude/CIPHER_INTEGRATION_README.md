# Claude Code Auto-Compact Cipher統合機能

## 概要
Claude Code のauto-compact発動時に、それまでの会話内容を自動的にCipherに記憶・復元するフック機能です。

## 機能
- **PreCompact Hook**: auto-compact前の会話内容を構造化プロンプトでCipherに保存
- **SessionStart Hook**: compact後の新セッションでCipherから記憶を復元
- **スマートタグ**: 言語検出、タスク分類、優先度評価による自動タグ付け
- **Claude CLI通信**: 非インタラクティブなCipher通信を実現

## ファイル構成
```
.claude/
├── settings.json                 # フック設定
├── hooks/
│   ├── cipher_memory_save.py    # PreCompactフック処理
│   ├── save_to_cipher.sh        # Bashラッパー（save用）
│   ├── cipher_memory_restore.py # SessionStartフック処理
│   ├── restore_from_cipher.sh   # Bashラッパー（restore用）
│   └── logs/
│       └── cipher_hook.log      # 動作ログ
└── README.md                    # 本ドキュメント
```

## 設定方法

### 1. settings.jsonを更新
```json
{
  "model": "opusplan",
  "hooks": {
    "PreCompact": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/save_to_cipher.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/restore_from_cipher.sh"
          }
        ]
      }
    ]
  }
}
```

### 2. ファイルを配置
テスト用の.claudeディレクトリから~/.claudeに配置：
```bash
cp -r .claude/* ~/.claude/
chmod +x ~/.claude/hooks/*.sh
```

## 動作確認

### テスト結果
✅ **Save機能テスト成功**:
- transcript解析: 5メッセージから6会話パートを抽出
- スマートタグ生成: `['auto-compact', 'project:temp-claude', 'lang:python', 'lang:json', 'lang:yaml', 'task:implementation', 'priority:high', 'status:planning']`
- Cipher保存: 1266文字の構造化プロンプトを正常保存
- 実行時間: 約23秒

⚠️ **Restore機能の制限**:
- Cipher検索でタイムアウト発生（10-20秒）
- 保存は成功するが検索に時間がかかる傾向
- 実環境では適宜タイムアウト調整が必要

## 生成されるメモリ構造

### 保存プロンプト形式
```markdown
Claude Code Auto-Compact Memory Archive

# Session Context
- Session ID: [session_id]
- Timestamp: [ISO時刻]
- Event: auto-compact triggered
- Project: [プロジェクト名]
- Working Directory: [作業ディレクトリ]

# Summary Request
[会話内容要約指示と分析対象内容]

# Memory Extraction Instructions
## 🎯 Project Goals & Current Status
## 📋 Active Tasks & Next Steps
## 🔧 Technical Context
## 📝 Important Context
## 🏷️ Classification Tags
```

### スマートタグシステム
- **プロジェクト**: `project:プロジェクト名`
- **言語検出**: `lang:python`, `lang:javascript` など
- **タスク分類**: `task:implementation`, `task:debugging` など
- **優先度**: `priority:high/medium/low`
- **状況**: `status:in-progress/completed/planning`
- **ソース**: `auto-compact`

## ログ確認
```bash
tail -f ~/.claude/hooks/logs/cipher_hook.log
```

## トラブルシューティング

### よくある問題

1. **Claude CLIが見つからない**
   ```bash
   which claude  # パス確認
   ```

2. **権限エラー**
   ```bash
   chmod +x ~/.claude/hooks/*.sh
   ```

3. **タイムアウト**
   - cipher_memory_restore.pyのtimeout値を調整（現在10秒）

4. **transcript解析失敗**
   - ログでメッセージ構造を確認
   - Claude Codeのバージョン確認

## 実装の特徴

### 技術的優位性
- **Non-blocking**: フック失敗でもセッション開始を妨げない
- **Structured Memory**: 分類された構造化プロンプトで検索性向上
- **Smart Tagging**: 自動タグ生成で効率的な記憶・検索
- **Error Resilience**: エラー時の適切なフォールバック

### セキュリティ考慮
- `--dangerously-skip-permissions`使用（自動化のため）
- ローカルファイル権限のみでの動作
- センシティブ情報は記録対象外

## 今後の改善点
- Cipher検索の高速化
- より精密なスマートタグアルゴリズム
- マルチセッション記憶の統合機能
- Web UI での記憶管理機能