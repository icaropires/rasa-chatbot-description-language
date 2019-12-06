from lark import Lark, InlineTransformer
import sys

class RasaTransformer(InlineTransformer):
    
    def start(self, blocks):
        return ['blocks', blocks]

    def blocks(self, *block):
        return [*block]

    def topics(self, *topic):
        return ['topics', list(topic)]
    
    def topic(self, text):
        return ['topic', str(text)]

    def header(self, type_, name):
        return ['header', [str(type_), str(name)]]

def _make_grammar():
    with open('grammar.lark') as fd:
        grammar = Lark(fd, parser='lalr', transformer=RasaTransformer())
    return grammar

def parse(src):
    parser = _make_grammar()

    return parser.parse(src)
