import argparse
from file_tree import Tree
from scrapper import Scrapper


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ChatGPT Code Summarizer",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--semi", action="store_true",
                        help="Create files for main directory only")
    parser.add_argument("--path", help="Location of code (default .\\code)")
    parser.add_argument("--prompt", help="Custom prompt for ChatGPT")
    args = parser.parse_args()
    config = vars(args)

    driver = Scrapper()
    driver.start()
    input("Please, press enter once you log in to chatgpt")
    try:
        driver.chatGPT(
            "Hello, can you help me summaries all the codes and file I give you?")
    except:
        print("Couldn't find chatGPT. The reasons could be following:")
        print("1. You closed the default tab opened")
        print("2. ChatGPT is not open with login in the default tab, please follow the steps in readme")


    if (config["path"]):
        FS = Tree(startpath=config["path"], semi=config["semi"])
    else:
        FS = Tree(semi=config["semi"])

    FS.fill()
    FS.sanitize()
    if (config["prompt"]):
        FS.fill_summaries(driver=driver, prompt=config["prompt"])
    else:
        FS.fill_summaries(driver=driver)
