##  ChatGPT Code Summarizer

A tool that uses ChatGPT and summary of summary algorithms to automatically generate summaries and documentation for any code repository.

### Requirments

- dataclasses
- selenium
- markdownify
- pyperclip (in case of linux, please also install xclip)
- gitignore_parser

PS: Add the file extensions you are using in the file extension_list.py

And add the file or directory in .gitignore in the root directory to remove the file for which you don't need summary

### Browser

Chrome browser is needed to run this

### Steps to run

1. Run index.py using python
2. Once it opens chrome, search for chatgpt in google and open link through searches (This is essential to bypass antibot)
3. After log into ChatGPT open it in first tab (default tab, otherwise bot will not work)
4. Enjoy while bot is doing your job. Expect min time = 2.5\*(number_of_folders + number_of_files) minutes

Watch this [video](https://youtu.be/1_DU9eZcjmQ) if you are not able to connect with chatgpt.

PS: Output generated will be in files in each directory (unless semi is true, see flags) by the name `readme_by_chatGPT.md`.

### Showcase

To showcase what my tool can do, I've generated complete documentation for one folder of the Twitter algorithm without any tweaks.

You could find it [here](https://github.com/Harshit-Ramolia/twitter-algorithm).

### Time

Currently this is using selenium to automate the chatGPT, but it can be changed with API.

### Flags

--semi : Create files for main directory only

--path : Location of code (default .\\code)

--prompt : Custom prompt for ChatGPT
