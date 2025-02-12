#!/usr/bin/env python3
import argparse
import json
import os

from .build_tree import build_json_directory
from .files import get_files_content
from .target_files import get_target_files


def main():
    parser = argparse.ArgumentParser(
        description="プロジェクト内の対象ファイル群を抽出し、Markdown ファイルに出力します。"
    )
    parser.add_argument(
        "project_dir", help="対象プロジェクトのルートディレクトリのパス"
    )
    parser.add_argument(
        "-o", "--output", default="summary.md", help="出力する Markdown ファイル名"
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_dir)
    target_files = get_target_files(project_root)

    print("---")
    for file in target_files:
        print(file)
    print("---")

    json_directory = build_json_directory(project_root, target_files)

    md_content = f"""
# Directory
```
{json.dumps(json_directory, indent=4, ensure_ascii=False)}
```

"""
    md_content += get_files_content(project_root, target_files)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Markdown ファイルが作成されました: {args.output}")


if __name__ == "__main__":
    main()
