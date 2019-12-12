def eval_(expr, env=None):
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

    head, *args = expr

    if head == "blocks":
        blocks = args[0]

        for block in blocks:
            eval_(block, env)

        return env

    elif head == "block":
        header, *topics = args

        type_, name = eval_(header, env)
        topics = eval_(*topics, env)

        if type_ == "intent":
            c_examples = [
                {"text": topic, "intent": name, "entities": []}
                for _, topic in topics
            ]

            env["rasa_nlu_data"]["common_examples"].extend(c_examples)

        return env

    elif head == "header":
        type_, name = args
        return type_, name

    elif head == "topics":
        topics = args
        return topics

    else:
        raise ValueError(f"Unexpected type on syntax tree: {head}")

    return env
