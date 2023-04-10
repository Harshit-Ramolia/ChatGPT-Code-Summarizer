dict = set([
    "c",
    "cgi",
    "pl",
    "class",
    "cpp",
    "cs",
    "h",
    "java",
    "php",
    "py",
    "sh",
    "swift",
    "vb"
])


def isExtension(extension: str) -> bool:
    return extension in dict

# https://gist.github.com/ppisarczyk/43962d06686722d26d176fad46879d41
# https://www.computerhope.com/issues/ch001789.htm#programming