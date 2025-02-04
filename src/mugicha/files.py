import os

def get_files_content(project_dir, file_paths):
    """
    プロジェクトディレクトリと、プロジェクトディレクトリからの相対パスのリストを受け取り、
    各ファイルの内容を以下の形式でひとつの文字列として返します。
    
    ## File.txt
    ```
    {content}
    ```
    
    ## File2.py
    ```
    {content}
    ```
    
    ※ファイルの読み込みに失敗した場合は、エラー内容を出力します。
    """
    output_lines = []
    for rel_path in file_paths:
        full_path = os.path.join(project_dir, rel_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except Exception as e:
            file_content = f"ファイルの読み込みに失敗しました: {e}"
        
        output_lines.append(f"## {rel_path}")
        output_lines.append("```")
        output_lines.append(file_content.rstrip())
        output_lines.append("```")
        output_lines.append("")  # 各ファイルの間に空行を追加

    result = "\n".join(output_lines)
    content = f"""{result}"""
    return content