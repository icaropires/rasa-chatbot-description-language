from parser import parse
import sys


def eval(x, env=None):
    """
    Avalia expressão.
    """

    if env is None:
        env = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

    head, *args = x

    if head == "blocks":
        blocks = []
        for block in args[0]:
            eval(block, env)
        return env

    elif head == "block":
        examples = []
        header, *topics = args
        type, content = eval(header, env)
        texts = eval(*topics)
        for text in texts:
            examples.append(
                {"text": text, "intent": content["intent"], "entities": []}
            )
        env["rasa_nlu_data"][type].extend(examples)
        return env

    elif head == "header":
        return eval(*args)

    elif head == "intent":
        return "common_examples", {"intent": args[0]}

    elif head == "topics":
        texts = []
        for topic in args[0]:
            texts.append(topic[1])
        return texts
    else:
        return None

    return env


test = sys.stdin.read()
print(eval(parse(test)))
