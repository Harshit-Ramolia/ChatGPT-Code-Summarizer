### Requirments

- dataclasses
- selenium
- markdownify
- pyperclip
- gitignore_parser

PS: Add the file extensions you are using in the file extension_list.py

### Browser

Chrome browser is needed to run this

### Steps to run

1. Run index.py using python
2. Once it opens chrome, log into google account
3. Then search for chatgpt in google and open link through searches (This is essential to bypass antibot)
4. After log into ChatGPT open it in first tab (default tab, otherwise bot will not work)
5. Enjoy while bot is doing your job

PS: Output generated will be in files in each directory (unless semi is true, see flags) by the name `readme_by_chatGPT.md`

### Flags
--semi : Create files for main directory only

--path : Location of code (default .\\code)

--prompt : Custom prompt for ChatGPT