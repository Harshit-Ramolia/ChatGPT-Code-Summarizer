import argparse
from file_tree import Tree
from scrapper import Scrapper
from pathlib import Path
import time

if __name__ == "__main__":
    startpath = str(Path(".\\code"))
    parser = argparse.ArgumentParser(description="ChatGPT Code Summarizer",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--semi", action="store_true",
                        help="Create files for main directory only")
    parser.add_argument("--path", help=f"Location of code (default {startpath})")
    parser.add_argument("--prompt", help="Custom prompt for ChatGPT")
    args = parser.parse_args()
    config = vars(args)

    if (config["path"]):
        FS = Tree(startpath=str(Path(config["path"])), semi=config["semi"])
    else:
        FS = Tree(semi=config["semi"])

    FS.fill()
    FS.sanitize()

    driver = Scrapper()
    driver.start()
    time.sleep(1)
    __temp = input(
        "Please, press enter once you log into chatgpt in default tab\n\n")
    
    print("Please wait, it may take a while.")
    
    try:
        driver.chatGPT(
            "Hello, can you help me summaries all the codes and file I give you?", repeat=False)
    except Exception as e:
        print(e)
        print("If error due selenium. The reasons could be following:")
        print("1. You closed the default tab opened")
        print("2. ChatGPT is not open with login in the default tab, please follow the steps in readme")
        exit(0)

    try:
        if (config["prompt"]):
            FS.fill_summaries(driver=driver, prompt=config["prompt"])
        else:
            FS.fill_summaries(driver=driver)
    except Exception as e:
        print(e)
        print("Some error occured, press enter to exit!")
