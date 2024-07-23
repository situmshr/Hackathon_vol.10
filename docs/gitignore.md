<img width="1971" alt="Screenshot 2024-07-23 at 14 57 18" src="https://github.com/user-attachments/assets/25e21776-a405-4f4b-9aa1-930fd03f49d8">


# `.git/info/` ディレクトリの下にある `exclude` ファイルに `".gitignore"` を追加する．

例）
```
$ echo ".gitignore" >> .git/info/exclude
```

上記コマンド実行後に，エディタを再起動する必要がある．

### その他，.gitignore に含めたほうが良いと思われるもの

- dp-env ... 仮想環境ディレクトリ
- __pycache__
- requirements.txt
- .DS_Store ... mac についてくる何かしら
