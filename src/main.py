import shutil
from pathlib import Path

from textnode import TextNode, TextType


def copy_all(source: Path, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    for file in source.rglob("*.*"):
        print(file)
        file: Path
        new_path: Path = dest.joinpath(file.relative_to(source))
        if not new_path.parent.exists():
            new_path.parent.mkdir(parents=True)
        shutil.copy(file, new_path)


def main():
    print("hello world")
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)
    project_root: Path = Path(__file__).absolute().parents[1]
    static_path: Path = project_root.joinpath("static")
    dest_path: Path = project_root.joinpath("public")
    copy_all(static_path, dest_path)


if __name__ == "__main__":
    main()
