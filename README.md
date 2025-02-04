mugicha
# Prepare
```bash
pip install pathspec toml
```

# Quick Start

```bash
git clone https://github.com/one2ndpiece/mugicha.git
```
execute mugicha
```bash
cd mugicha
python -m run src/mugicha/__init__.py
```

# mugicha Install
whlファイルは適切なものをダウンロードしてください。
```bash
git clone https://github.com/one2ndpiece/mugicha.git
cd mugicha
pip install dist/mugicha-0.0.1-py3-none-any.whl
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
