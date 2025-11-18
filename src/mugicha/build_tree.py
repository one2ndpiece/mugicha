from __future__ import annotations

import os
from typing import Any


def build_json_directory(root: str, file_list: list[str]) -> dict:
    """
    root: ルートディレクトリの名前(例:"mugicha")
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

    # 内部表現として、各ディレクトリは辞書で表現する
    tree = {}

    for path in file_list:
        is_dir = path.endswith('/')
        relative_path = path.rstrip('/') if is_dir else path
        if not relative_path:
            continue

        parts = relative_path.split('/')
        current = tree

        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                if is_dir:
                    if part not in current:
                        current[part] = {}
                else:
                    if part not in current:
                        current[part] = None
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]

    # 内部ツリー構造を目的の形式に変換するためのヘルパー関数
    def convert_node(node: dict[str, Any]) -> list[str | dict[str, Any]]:
        items = []
        for key in sorted(node.keys()):
            value = node[key]
            if value is None:
                items.append(key)
            else:
                items.append({key + '/': convert_node(value)})
        return items

    # ルートディレクトリをキー(末尾に "/" を付ける)とする
    return {base_root + '/': convert_node(tree)}
