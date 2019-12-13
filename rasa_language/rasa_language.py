from .parser import parse


class RasaLanguage:
    def __init__(self):
        self.nlu = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        self.domain = {}

        self.stories = {}

    def process(self, text):
        self.eval(parse(text))

    def eval(self, expr):
        head, *args = expr

        if head == "blocks":
            blocks = args

            for block in blocks:
                self.eval(block)

        elif head == "block":
            examples = []
            nlu_type = ""
            header, *topics = args

            type_, name = self.eval(header)
            topics = self.eval(*topics)

            if type_ == "intent":
                nlu_type = "common_examples"
                for topic in topics:
                    for element in topic[1:]:
                        intent = self.eval(element)
                        if intent:
                            intent_text, entities = intent
                            if entities:
                                start, end, value, entity = entities[0]
                                entities = {
                                    "start": start,
                                    "end": end,
                                    "value": value,
                                    "entity": entity,
                                }
                            examples.append(
                                {
                                    "text": intent_text,
                                    "intent": name,
                                    "entities": entities,
                                }
                            )
            elif type_ == "synonym":
                nlu_type = "entity_synonyms"
                examples.append({"value": name, "synonyms": topics})
            elif type_ == "regex":
                nlu_type = "regex_features"
                for topic in topics:
                    examples.append({"name": name, "pattern": topic})
            elif type_ == "lookup":
                nlu_type = "lookup_tables"
                examples.append({"name": name, "elements": topics})

            self.nlu["rasa_nlu_data"][nlu_type].extend(examples)

        elif head == "header":
            type_, name = args
            return type_, name

        elif head == "text":
            text, *entities = args
            return text, entities

        elif head == "synonyms":
            for value, _, synonyms in args[0]:
                self.nlu["rasa_nlu_data"]["entity_synonyms"].extend(
                    [{"value": value, "synonyms": synonyms}]
                )

        elif head == "topics":
            topics = args
            return topics

        else:
            raise ValueError(f"Unexpected type on syntax tree: {head}")

    def dump_files(self, bot_dir):
        self._dump_nlu(bot_dir)
        self._dump_domain(bot_dir)
        self._dump_stories(bot_dir)

    def _dump_nlu(self, bot_dir):
        ...

    def _dump_domain(self, bot_dir):
        ...

    def _dump_stories(self, bot_dir):
        ...
