from lark import Lark, InlineTransformer
from pathlib import Path


class RasaTransformer(InlineTransformer):
    def start(self, blocks):
        return blocks

    def blocks(self, *blocks):
        return ["blocks", *blocks]

    def block(self, *block):
        return ["block", *block]

    def topics(self, *topics):
        return ["topics", *topics]

    def topic(self, marker, *topic):
        text = ["text", ""]
        synonyms = ["synonyms", []]
        intents = ["intents", []]
        full_topic = []
        text_len = 0

        for ix, t in enumerate(topic):
            type_, *content = t
            text[1] += content[0]
            if type_ == "synonym":
                # se o sinônimo não aparece na primeira posição
                if ix > 0:
                    start = text_len
                    end = start + len(content[0])
                    text.append([start, end, content[0], content[1]])
                else:
                    start = 0
                    end = len(content[0])
                    text.append([start, end, content[0], content[1]])

                synonyms[1].append(t[1:])
            elif type_ == "intent":
                if ix > 0:
                    start = text_len
                    end = start + len(content[0])
                    text.append([start, end, content[0], content[1]])
                else:
                    start = 0
                    end = len(content[0])
                    text.append([start, end, content[0], content[1]])
                intents[1].append(t[1:])
            text_len += len(content[0])
        full_topic = [str(marker), text]
        if synonyms[1]:
            full_topic.append(synonyms)
        if intents[1]:
            full_topic.append(intents)
        return full_topic

    def element(self, content):
        return content

    def intent(self, name, intent_name):
        return ["intent", str(name), str(intent_name)]

    def synonym(self, name, *synonyms):
        entity, *synonyms = [str(s) for s in synonyms]
        return ["synonym", str(name), entity, synonyms]

    def text(self, content):
        return ["text", str(content)]

    def header(self, type_, name):
        return ["header", str(type_), str(name)]

    def header_story(self, name):
        return ["header_story", str(name)]


def _make_grammar():
    path = Path(__file__).parent / "grammar.lark"
    with open(path) as fd:
        grammar = Lark(fd, parser="lalr", transformer=RasaTransformer())
    return grammar


def parse(src):
    return parser.parse(src)


parser = _make_grammar()
