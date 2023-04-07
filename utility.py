import gitignore_parser
from dataclasses import dataclass, field
from extension_list import isExtension
from typing import List


def is_gitignored(path):
    parser = gitignore_parser.parse_gitignore('.\code\.gitignore')
    return parser(path)


@dataclass
class Node:
    name: str = None
    root: str = None
    childrens: dict[str, "Node"] = field(default_factory=dict)
    files: List[str] = field(default_factory=list)
    no_files: bool = True
    full_summary: str = ""
    files_summary: List[str] = field(default_factory=list)

    # def __repr__(self):
    #     print(self.name, self.no_files)
    #     for name in self.childrens:
    #         print(self.childrens[name])
    #     return ""


@dataclass
class Tree:
    root: Node = field(default=None)

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

    def add(self, root: str, dirs: List[str], files: List[str]) -> None:
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

    def sanitize(self) -> None:
        self.__fill_no_files(self.root)
        self.root = self.__remove_no_files(self.root)
