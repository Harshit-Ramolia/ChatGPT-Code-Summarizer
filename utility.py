import gitignore_parser
from dataclasses import dataclass, field
from extension_list import isExtension
from scrapper import Scrapper
from typing import List
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


@dataclass
class Node:
    name: str = None
    root: str = None
    childrens: dict[str, "Node"] = field(default_factory=dict)
    files: List[str] = field(default_factory=list)
    no_files: bool = True
    full_summary: str = ""
    files_summary: List[str] = field(default_factory=list)


@dataclass
class Tree:
    startpath: str = ".\code"
    root: Node = field(default=None, init=None)

    def __make_node(self, root: str, name: str, dirs: List[str], files: List[str]) -> Node:
        files = list(filter(lambda x: isExtension(x.split(".")[1]), files))
        files = list(filter(lambda x: not is_gitignored(root+"\\"+x), files))
        new_node = Node(name=name, root=root, files=files)
        for folders in dirs:
            new_node.childrens[folders] = None
        return new_node

    def __fill_no_files(self, node: Node) -> bool:
        do_child_have_files = False
        for name in node.childrens:
            val = self.__fill_no_files(node.childrens[name])
            do_child_have_files = do_child_have_files or val
        do_current_have_files = len(node.files) > 0
        have_files = do_child_have_files or do_current_have_files
        node.no_files = not have_files
        return have_files

    def __remove_no_files(self, node: Node) -> Node:
        if (node.no_files == True):
            return None

        remove = []
        for name in node.childrens:
            new_node = self.__remove_no_files(node.childrens[name])
            if (new_node != None):
                node.childrens[name] = new_node
            else:
                remove += [name]

        for name in remove:
            del node.childrens[name]

        return node

    def __add(self, root: str, dirs: List[str], files: List[str]) -> None:
        current_node = self.root
        path = root[1:].split('\\')[1:]
        if (current_node == None):
            new_node = self.__make_node(
                root=root, name=path[0], dirs=dirs, files=files)
            self.root = new_node
            return
        for name in path[1:]:
            if (current_node.childrens[name] == None):
                new_node = self.__make_node(
                    root=root, name=name, dirs=dirs, files=files)
                current_node.childrens[name] = new_node
                return
            current_node = current_node.childrens[name]

    def fill(self) -> None:
        startpath = self.startpath
        assert os.path.exists(
            startpath), f"Directory {startpath} doesn't exist"
        for ele in os.walk(startpath):
            self.__add(*ele)

    def sanitize(self) -> None:
        self.__fill_no_files(self.root)
        self.root = self.__remove_no_files(self.root)

    def __summarize(self, node: Node, driver: Scrapper, prompt: str) -> None:
        children_summaries = []
        for name in node.childrens:
            response = self.__summarize(node.childrens[name], driver)
            response = f"The following is the documentaion and summary for directory {name}\n\n {response} \n\n"
            children_summaries += [response]
            print(f"completed dir = {node.root}\\{name}")

        files_summary = []
        for file in node.files:
            input = file_content(node.root+"\\"+file)
            input += f"\n\n{prompt}\n\n"
            response = driver.chatGPT(input)
            response = f"The following is the documentaion and summary for file {file}\n\n {response} \n\n"
            files_summary += [response]
            print(f"completed file = {node.root}\\{file}")

        node.files_summary = files_summary

        input = f"\n\n{prompt}\n\n"
        summary = "\n".join(children_summaries+files_summary)

        response = driver.chatGPT(summary+input)
        file_create(f"{node.root}\document.md", response)
        node.full_summary = response
        return response

    def fill_summaries(self, driver: Scrapper, prompt: str = "Can you please summarize the above content in markdown format also use tables wherever feels good. Please explain what the code does, what parameters it takes and what it returns. Keep it simple. Please also ensure that the response is provided in markdown format so that I can easily copy and paste it to a file or document. Thank you. \n\n Please in markdown format. This is very important.") -> None:
        self.__summarize(self.root, driver, prompt)
