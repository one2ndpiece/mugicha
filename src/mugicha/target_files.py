import os

import pathspec
import toml


def load_gitignore(project_root):
    """
    プロジェクトルートにある .gitignore を読み込み、
    そのパターンから pathspec オブジェクトを返します。
    存在しない場合は None を返します。
    """
    gitignore_path = os.path.join(project_root, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            # 空行やコメント行を除外してパターンを取得
            patterns = [
                line.rstrip()
                for line in f
                if line.strip() and not line.lstrip().startswith("#")
            ]
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return None


def load_mugicha(project_root):
    """
    プロジェクトルートにある mugicha.toml を読み込み、
    ignore 用と show 用のパターンから pathspec オブジェクトを生成して返します。
    存在しない場合は (None, None) を返します。

    mugicha.toml の例:

        ignore = ["build/", "tmp/", "*.log"]
        show   = ["tmp/important.log"]
    """
    mugicha_path = os.path.join(project_root, "mugicha.toml")
    ignore_spec = None
    show_spec = None
    if os.path.exists(mugicha_path):
        try:
            config = toml.load(mugicha_path)
            ignore_patterns = config.get("ignore", [])
            show_patterns = config.get("show", [])
            if isinstance(ignore_patterns, list) and ignore_patterns:
                ignore_spec = pathspec.PathSpec.from_lines(
                    "gitwildmatch", ignore_patterns
                )
            if isinstance(show_patterns, list) and show_patterns:
                show_spec = pathspec.PathSpec.from_lines("gitwildmatch", show_patterns)
        except Exception as e:
            print(f"mugicha.toml の読み込みエラー: {e}")
    return ignore_spec, show_spec


def get_all_files(project_root):
    """
    プロジェクト内の全ファイルの相対パス（UNIX形式）リストを返します。
    """
    file_list = []
    for dirpath, _, filenames in os.walk(project_root):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, project_root)
            # OS依存のパス区切りを "/" に統一
            rel_path = rel_path.replace(os.sep, "/")
            file_list.append(rel_path)
    return file_list


def get_target_files(project_root):
    """
    ・.gitignore による除外ルールを反映して対象となるファイルのリストを取得します。
        → 全ファイル集合から、.gitignore のパターンにマッチするファイルを除外
    ・mugicha.toml の ignore ルールによる除外を反映して対象となるファイルのリストを取得します。
        → 全ファイル集合から、mugicha の ignore パターンにマッチするファイルを除外
    ・上記2つのルールの結果のORを対象ファイルとします。
    ・さらに、mugicha.toml の show ルールにマッチするファイルを追加します。
    """
    all_files = get_all_files(project_root)

    # .gitignore の場合:
    gitignore_spec = load_gitignore(project_root)
    excluded_files = set()  # ここを set() に変更
    if gitignore_spec:
        # .gitignore にマッチするファイル（除外対象）
        gitignore_excluded = set(gitignore_spec.match_files(all_files))
        excluded_files.update(gitignore_excluded)  # += ではなく update を使う

    # mugicha.toml の ignore の場合:
    mugicha_ignore_spec, mugicha_show_spec = load_mugicha(project_root)
    if mugicha_ignore_spec:
        mugicha_excluded = set(mugicha_ignore_spec.match_files(all_files))
        excluded_files.update(mugicha_excluded)  # または .union(mugicha_excluded)

    target_files = set(all_files) - excluded_files

    # mugicha.toml の show ルールにマッチするファイルを追加（除外ルールを上書き）
    if mugicha_show_spec:
        mugicha_show_files = set(mugicha_show_spec.match_files(all_files))
    else:
        mugicha_show_files = set()

    target_files = target_files.union(mugicha_show_files)

    return sorted(target_files)
