from lark import Lark, InlineTransformer
from pathlib import Path


class RasaTransformer(InlineTransformer):
    def start(self, blocks):
        return blocks

    def blocks(self, *block):
        return ["blocks", [*block]]

    def block(self, *block):
        return ["block", *block]

    def topics(self, *topic):
        print('-----------', topic)
        return ["topics", [str(t) for t in topic]]

    def header(self, type_, name):
        return ["header", [str(type_), str(name)]]


def _make_grammar():
    path = Path(__file__).parent / "grammar.lark"
    with open(path) as fd:
        grammar = Lark(fd, parser="lalr", transformer=RasaTransformer())
    return grammar


def parse(src):
    return parser.parse(src)


parser = _make_grammar()
