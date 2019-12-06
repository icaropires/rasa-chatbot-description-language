from .parser import parse as parse_src
from . import __version__ as version


def main():
    ast = parse_src(src)
    print(ast)


if __name__ == '__main__':
    main()
