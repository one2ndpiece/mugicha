mugicha
# installation
```bash
uv add --dev git+https://github.com/one2ndpiece/mugicha.git
```


# mugicha.toml
mugicha.toml は以下のように設定してください。
ワイルドカードもある程度サポートしています。
```toml
ignore = [
    "file.txt",
    "dir/",
]
show = [
    "file.txt",
    "dir/",
]
```

## 処理の順番
1. 全ファイルを取得
2. プロジェクトのルートにある.gitignoreに相当するファイルを除外
3. mugicha.tomlのignoreに記載されているファイルを除外
4. mugicha.tomlのshowに記載されているファイルを追加

出力されたファイルを見て、適宜ignoreやshowに追加してください。

mugicha.tomlのignoreでホワイトリストを書くこともある程度可能です。

## ignoreリストに入れた方が良さそうなファイル・ディレクトリ
```
.gitignore
.git/
.venv/
```
