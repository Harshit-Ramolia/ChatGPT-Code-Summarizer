import gitignore_parser


def is_gitignored(path):
    print(path)
    parser = gitignore_parser.parse_gitignore('.\code\.gitignore')
    return parser(path)