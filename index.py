from utility import Tree
import os

FileStruct = Tree()
startpath = ".\code"
for ele in os.walk(startpath):
    FileStruct.add(*ele)
FileStruct.sanitize()
