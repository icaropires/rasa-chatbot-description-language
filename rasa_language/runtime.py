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
    print("xxxx", x)
    head, *args = x

    if head == "blocks":
        for block in args[0]:
            eval(block, env)
        return env

    elif head == "block":
        examples = []
        header, *topics = args
        type, name = eval(header, env)
        values = eval(*topics)
        if type == "common_examples":
            for value in values:
                examples.append(
                    {"text": value, "intent": name, "entities": []}
                )
        elif type == "entity_synonyms":
            examples.append({"value": name, "synonyms": values})

        elif type == "regex_features":
            for value in values:
                examples.append({"name": name, "pattern": value})
        elif type == "lookup_tables":
            examples.append({"name": name, "elements": values})

        env["rasa_nlu_data"][type].extend(examples)
        print("eee", env)
        return env

    elif head == "header":
        return eval(*args)

    elif head == "intent":
        return "common_examples", args[0]

    elif head == "synonym":
        return "entity_synonyms", args[0]

    elif head == "regex":
        return "regex_features", args[0]

    elif head == "lookup":
        return "lookup_tables", args[0]

    elif head == "topics":
        values = []
        for topic in args[0]:
            values.append(topic)
        return values
    else:
        return None

    return env


test = sys.stdin.read()
print(eval(parse(test)))
