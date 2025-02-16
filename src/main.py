import shutil
from pathlib import Path

from markdown_documents import extract_tile, markdown_to_html_node


def copy_all(source: Path, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    for file in source.rglob("*.*"):
        file: Path
        new_path: Path = dest.joinpath(file.relative_to(source))
        if not new_path.parent.exists():
            new_path.parent.mkdir(parents=True)
        shutil.copy(file, new_path)


def gerenate_page_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path
):
    for file in dir_path_content.rglob("*.md"):
        new_path: Path = dest_dir_path.joinpath(
            file.relative_to(dir_path_content)
        ).with_suffix(".html")

        generate_page(file, template_path, new_path)


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "rt") as markdown:
        raw_content = markdown.read()
        content = markdown_to_html_node(raw_content).to_html()
    title = extract_tile(raw_content)
    with open(template_path, "rt") as template_stream:
        template: str = template_stream.read()
    template = template.replace("{{ Title }}", title)
    html = template.replace("{{ Content }}", content)
    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True)
    with open(dest_path, "wt") as file:
        file.write(html)


def main():
    project_root: Path = Path(__file__).absolute().parents[1]
    static_path: Path = project_root.joinpath("static")
    dest_path: Path = project_root.joinpath("public")
    copy_all(static_path, dest_path)
    content_path: Path = project_root.joinpath("content")
    template_path: Path = project_root.joinpath("template.html")
    gerenate_page_recursive(content_path, template_path, dest_path)


if __name__ == "__main__":
    main()
