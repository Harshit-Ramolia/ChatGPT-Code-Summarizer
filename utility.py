import gitignore_parser
import os


def is_gitignored(path):
    parser = gitignore_parser.parse_gitignore('.\code\.gitignore')
    return parser(path)


def file_content(path):
    assert os.path.exists(path), f"File {path} doesn't exist"
    file = open(path, "r")
    return file.read()


def file_create(path, content):
    try:
        file = open(path, "x")
    except:
        file = open(path, "w")
    file.write(content)
