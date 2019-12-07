from .parser import parse as parse_src
from sys import argv, exit
from . import __version__ as version


def main():
    if len(argv) <= 1:
        print("Wrong Usage")
        exit(1)

    with open(argv[1]) as input_txt:
        ast = parse_src(input_txt.read())


if __name__ == "__main__":
    main()
