import gitignore_parser
import os


def is_gitignored(path: str, gitpath: str) -> bool:
    try:
        parser = gitignore_parser.parse_gitignore(gitpath)
        return parser(path)
    except:
        return False


def file_content(path: str) -> str:
    assert os.path.exists(path), f"File {path} doesn't exist"
    file = open(path, "r")
    return file.read()


def file_create(path: str, content: str) -> None:
    try:
        file = open(path, "x")
    except:
        file = open(path, "w")
    file.write(content)
