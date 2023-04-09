from dataclasses import dataclass, field
from extension_list import isExtension
from scrapper import Scrapper
from typing import List
from utility import *
from tqdm import tqdm
from pathlib import Path


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
    startpath: str = str(Path(".\\code"))
    root: Node = field(default=None, init=None)
    semi: bool = False

    def __make_node(self, root: str, name: str, dirs: List[str], files: List[str]) -> Node:
        dirs = list(filter(lambda x: x[0] != ".", dirs))        
        files = list(filter(lambda x: not is_gitignored(
            Path.joinpath(Path(root), x), Path.joinpath(Path(self.startpath), ".gitignore")), files))
        files = list(filter(lambda x: isExtension(x.split(".")[1]), files))
        
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
        root_path = Path(root)
        current_node = self.root
        path = list(root_path.parts)
        if (current_node == None):
            new_node = self.__make_node(
                root=str(root_path), name=self.startpath, dirs=dirs, files=files)
            self.root = new_node
            return
        for name in path[len(list(Path(self.startpath).parts)):]:
            if (name not in current_node.childrens):
                return
            if (current_node.childrens[name] == None):
                new_node = self.__make_node(
                    root=str(root_path), name=name, dirs=dirs, files=files)
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

    def __total(self, node: Node) -> int:
        count = 0
        for name in node.childrens:
            count += self.__total(node.childrens[name])

        count += len(node.files)

        count += 1

        return count

    def __summarize(self, node: Node, driver: Scrapper, prompt: str, pbar: tqdm) -> None:
        children_summaries = []
        for name in node.childrens:
            response = self.__summarize(
                node.childrens[name], driver, prompt, pbar)
            response = f"The following is the documentaion and summary for directory {name}\n\n {response} \n\n"
            children_summaries += [response]
            print(f"completed dir = {node.root}\\{name}")

        files_summary = []
        for file in node.files:
            input = file_content(node.root+"\\"+file)
            input += f"\n\n{prompt}\n\n"
            response = driver.chatGPT(input)
            pbar.update(1)
            response = f"The following is the documentaion and summary for file {file}\n\n {response} \n\n"
            files_summary += [response]
            print(f"completed file = {node.root}\\{file}")

        node.files_summary = files_summary

        input = f"\n\n{prompt}\n\n"
        summary = "\n".join(children_summaries+files_summary)

        response = driver.chatGPT(summary+input)
        pbar.update(1)
        if (not self.semi):
            if (len(response) >= 300):
                file_create(f"{node.root}\\readme_by_ChatGPT.md", response)
                node.full_summary = response
                return response
            else:
                file_create(f"{node.root}\\readme_by_ChatGPT.md", summary)
                node.full_summary = summary
                return summary

    def fill_summaries(self, driver: Scrapper, prompt: str = "Can you please summarize the above content in markdown format also use tables wherever feels good. Please explain what the code does, what parameters it takes and what it returns. Keep it simple. Please also ensure that the response is provided in markdown format so that I can easily copy and paste it to a file or document. Thank you.") -> None:
        total = self.__total(self.root)
        print(total)
        # pbar = tqdm(total=total)
        # self.__summarize(self.root, driver, prompt, pbar)
        # if (self.semi):
        #     file_create(f"{self.root.root}\\readme_by_ChatGPT.md",
        #                 self.root.full_summary)
