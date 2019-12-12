from lark import Lark, InlineTransformer
from pathlib import Path


class RasaTransformer(InlineTransformer):
    def start(self, blocks):
        return blocks

    def blocks(self, *blocks):
        return ["blocks", [*blocks]]

    def block(self, *block):
        return ["block", *block]

    def topics(self, *topics):
        return ["topics", *topics]

    def topic(self, marker, topic):
        return [str(marker), str(topic)]

    def header(self, type_, name):
        return ["header", str(type_), str(name)]


def _make_grammar():
    path = Path(__file__).parent / "grammar.lark"
    with open(path) as fd:
        grammar = Lark(fd, parser="lalr", transformer=RasaTransformer())
    return grammar


def parse(src):
    return parser.parse(src)


parser = _make_grammar()
