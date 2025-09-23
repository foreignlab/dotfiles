# Claude Code Auto-Compact Cipher Integration

Auto-Compact発動時に会話内容をCipherに自動保存するフック実装です。

## 概要

Claude Codeのコンテキストが満杯になってauto-compactが発動する際に、それまでの会話内容を自動的にCipherに記憶させる仕組みです。これにより、セッション間での文脈保持が改善されます。

## ファイル構成

```
.claude/
├── settings.json              # フック設定
├── hooks/
│   ├── save_to_cipher.sh     # Bashラッパースクリプト
│   ├── cipher_memory_save.py # メイン処理（Python）
│   └── logs/
│       └── cipher_hook.log   # 実行ログ
├── test_hook.sh              # テストスクリプト
└── README.md                 # このファイル
```

## 動作フロー

1. Claude Codeでauto-compactが発動
2. PreCompact Inputフックが呼び出される
3. `save_to_cipher.sh`が実行される
4. `cipher_memory_save.py`がトランスクリプトを解析
5. 重要な会話内容をCipherに保存

## 設定内容

### settings.json

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
    ]
  }
}
```

## 実装詳細

### save_to_cipher.sh

- PreCompact Inputイベントのエントリーポイント
- エラーハンドリングとログ出力
- Pythonスクリプトの実行

### cipher_memory_save.py

- PreCompact Input JSONの解析
- triggerが"auto"の場合のみ処理
- トランスクリプトファイルからの会話内容抽出
- Cipherへのメモリ保存（現在はシミュレーション）

## インストール手順

1. この`.claude`ディレクトリの内容を`~/.claude`にコピー
2. スクリプトに実行権限を付与：
   ```bash
   chmod +x ~/.claude/hooks/save_to_cipher.sh
   chmod +x ~/.claude/hooks/cipher_memory_save.py
   ```
3. Claude Codeを再起動

## テスト実行

```bash
# テストスクリプトを実行
./test_hook.sh
```

テストでは以下を確認できます：
- auto triggerでの正常動作
- manual triggerでのスキップ
- ログ出力の確認

## 制限事項と今後の改善

### 現在の制限
- Cipherへの実際のMCP通信は未実装（シミュレーション）
- 機密情報のフィルタリング機能なし
- エラー時のリトライ機能なし

### 今後の改善予定
- 実際のMCP通信実装
- 機密情報の自動フィルタリング
- ログローテーション機能
- より詳細なエラーハンドリング

## ログ確認

実行ログは以下で確認できます：
```bash
tail -f ~/.claude/hooks/logs/cipher_hook.log
```

## トラブルシューティング

### よくある問題

1. **スクリプトが実行されない**
   - 実行権限を確認：`ls -la ~/.claude/hooks/`
   - パスが正しいことを確認

2. **Pythonエラー**
   - Python3がインストールされていることを確認
   - 必要なモジュールがインストールされていることを確認

3. **ログが出力されない**
   - ログディレクトリの権限を確認
   - Claude Codeの再起動を試行

### デバッグ方法

1. テストスクリプトで動作確認：
   ```bash
   ./test_hook.sh
   ```

2. 手動でフックを実行：
   ```bash
   echo '{"session_id":"test","transcript_path":"/path/to/transcript.jsonl","hook_event_name":"PreCompact","trigger":"auto","custom_instructions":""}' | ~/.claude/hooks/save_to_cipher.sh
   ```

3. ログファイルを確認：
   ```bash
   cat ~/.claude/hooks/logs/cipher_hook.log
   ```

## セキュリティ注意事項

- フックは自動的に実行されるため、スクリプトの内容を十分確認してください
- ログファイルには機密情報が含まれる可能性があります
- 定期的にログファイルのクリーンアップを行ってください