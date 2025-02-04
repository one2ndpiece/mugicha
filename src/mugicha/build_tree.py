import os

def build_json_directory(root, file_list):
    """
    root: ルートディレクトリの名前（例："mugicha"）
    file_list: ルート以下のファイル・ディレクトリの相対パス一覧
            ディレクトリは末尾に "/" が付いているものとする
            例:
            [
                ".devcontainer/",
                ".git/",
                ".gitattributes",
                ".gitignore",
                ".python-version",
                ".venv/",
                "README.md",
                "dev-only/",
                "mugicha.toml",
                "pyproject.toml",
                "src/main.py",
                "temp/",
                "uv.lock"
            ]
    戻り値: 指定の形式のディレクトリ構造を表現した辞書
    """
    base_root = os.path.basename(os.path.normpath(root))

    # 内部表現として、各ディレクトリは辞書で表現し、"__order__" キーで追加順序を記録する
    tree = {"__order__": []}

    for path in file_list:
        # ファイルかディレクトリか判定（末尾が "/" の場合はディレクトリ）
        is_dir = path.endswith("/")
        # ディレクトリの場合は末尾の "/" を一時的に除去してパーツに分解する
        relative_path = path.rstrip("/") if is_dir else path
        if not relative_path:
            continue  # 空文字は無視

        parts = relative_path.split("/")
        current = tree

        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # 最後のパーツ：ディレクトリ or ファイルの登録
                if is_dir:
                    if part not in current:
                        current[part] = {"__order__": []}
                        current["__order__"].append(part)
                else:
                    if part not in current:
                        current[part] = None  # ファイルの場合は値を None とする
                        current["__order__"].append(part)
            else:
                # 中間パーツは必ずディレクトリ
                if part not in current:
                    current[part] = {"__order__": []}
                    current["__order__"].append(part)
                current = current[part]

    # 内部ツリー構造を目的の形式に変換するためのヘルパー関数
    def convert_node(node):
        items = []
        for key in node.get("__order__", []):
            value = node[key]
            if value is None:
                # ファイルの場合はそのまま文字列として追加
                items.append(key)
            else:
                # ディレクトリの場合は、キー名に "/" を付け、その中身を再帰的に変換
                items.append({key + "/": convert_node(value)})
        return items

    # ルートディレクトリをキー（末尾に "/" を付ける）とする
    return {base_root + "/": convert_node(tree)}
