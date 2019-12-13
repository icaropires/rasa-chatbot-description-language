import json
import yaml
import click
import pathlib
from .parser import parse


class RasaLanguage:
    def __init__(self):
        self.parse = parse

        self.nlu = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        self.domain = {
            "slots": [],
            "entities": [],
            "intents": [],
            "templates": {},
            "actions": [],
        }

        self.stories = {}

    def process(self, text):
        self._eval(self.parse(text))

    def _eval(self, expr):
        head, *args = expr

        if head == "blocks":
            blocks = args

            for block in blocks:
                self._eval(block)

        elif head == "block":
            header, *topics = args

            type_, name = self._eval(header)
            topics = self._eval(*topics)

            block_evals = {
                "intent": self._eval_intents,
                "utter": self._eval_utters,
                "synonym": self._eval_synonym,
                "regex": self._eval_regexes,
                "lookup": self._eval_lookups,
                "story": self._eval_stories,
            }

            block_evals[type_](name, topics)

        elif head == "header":
            type_, name = args
            return type_, name

        elif head == "header_story":
            name = args[0]
            return "story", name

        elif head == "text":
            text, *entities = args
            return text, entities

        elif head == "synonyms":
            for value, _, synonyms in args[0]:
                self.nlu["rasa_nlu_data"]["entity_synonyms"].extend(
                    [{"value": value, "synonyms": synonyms}]
                )

        elif head == "intents":
            ...

        elif head == "topics":
            topics = args
            return topics

        else:
            raise ValueError(f"Unexpected type on syntax tree: {head}")

    def _eval_regexes(self, name, topics):
        self.nlu["rasa_nlu_data"]["regex_features"].extend(
            [{"name": name, "pattern": topic} for topic in topics]
        )

    def _eval_lookups(self, name, topics):
        self.nlu["rasa_nlu_data"]["lookup_tables"].extend(
            {"name": name, "elements": topics}
        )

    def _eval_synonym(self, name, topics):
        self.nlu["rasa_nlu_data"]["entity_synonyms"].extend(
            {"value": name, "synonyms": topics}
        )

    def _eval_utters(self, name, topics):
        texts = [{"text": topic[1]} for _, topic in topics]

        utter_name = f"utter_{name}"

        self.domain["templates"][utter_name] = texts
        self.domain["actions"].append(utter_name)

    def _eval_intents(self, name, topics):
        examples = []
        intent_entities = []

        for topic in topics:
            for element in topic[1:]:
                intent = self._eval(element)
                if intent:
                    intent_text, entities = intent

                    if entities:
                        for entity_ in entities:
                            start, end, value, entity = entity_
                            entities = {
                                "start": start,
                                "end": end,
                                "value": value,
                                "entity": entity,
                            }
                            intent_entities.append(entities)

                    examples.append(
                        {
                            "text": intent_text,
                            "intent": name,
                            "entities": intent_entities,
                        }
                    )
        self.nlu["rasa_nlu_data"]["common_examples"].extend(examples)
        self.domain["intents"].append(name)

    def _eval_stories(self, name, topics):
        story_steps = []

        for marker, topic in topics:
            step = {}

            if marker == ">":
                if (
                    len(story_steps) > 1
                    and story_steps[-1]["type"] == "intent"
                ):
                    raise ValueError(
                        f"Invalid story: '{name}'." " Two consecutive intents!"
                    )

                step["type"] = "intent"

                intents = self.nlu["rasa_nlu_data"]["common_examples"]

                for intent in intents:
                    intent_text = topic[1]
                    if intent["text"] == intent_text:
                        step["name"] = intent["intent"]
                        break

                step["entities"] = {}  # TODO: Add real entities

            elif marker == "-":
                step["type"] = "action"
                templates = self.domain["templates"]

                for utter, samples in templates.items():
                    for sample in samples:
                        topic_text = topic[1]
                        if sample["text"] == topic_text:
                            step["name"] = utter
                            break
            else:
                raise ValueError(f"Invalid marker '{marker}'")

            story_steps.append(step)

        self.stories[name] = story_steps

    def dump_files(self, bot_dir):
        self._dump_nlu(bot_dir)
        self._echo_succesfully_dumped("NLU")

        self._dump_stories(bot_dir)
        self._echo_succesfully_dumped("Stories")

        self._dump_domain(bot_dir)
        self._echo_succesfully_dumped("Domain")

    def _dump_nlu(self, bot_dir):
        path = pathlib.Path(bot_dir) / "data" / "nlu.json"

        with open(path, "w") as f:
            json.dump(
                self.nlu, f, ensure_ascii=False, indent=4, sort_keys=True
            )

    def _dump_domain(self, bot_dir):
        path = pathlib.Path(bot_dir) / "domain.yml"

        # Remove keys with empty values
        self.domain = {k: v for k, v in self.domain.items() if v}

        with open(path, "w") as f:
            stream = yaml.dump(
                self.domain,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

            # Insert blank lines between top level keys
            for key in tuple(self.domain.keys())[1:]:
                stream = stream.replace(key, f"\n{key}")

            f.write(stream)

    def _dump_stories(self, bot_dir):
        path = pathlib.Path(bot_dir) / "stories.md"

        with open(path, "w") as f:
            f.write(self._get_story_as_md())

    @staticmethod
    def _echo_succesfully_dumped(filename):
        click.secho(
            f"{filename} file generated succesfully!", fg="green", bold=True
        )

    def _get_story_as_md(self):
        md = ""

        for story_name, topics in self.stories.items():
            md += f"## {story_name}\n"

            for topic in topics:
                if topic["type"] == "intent":
                    md += f"* {topic['name']}"

                    md += (
                        json.dumps(topic["entities"], ensure_ascii=False)
                        if topic["entities"]
                        else ""
                    )

                    md += "\n"
                elif topic["type"] == "action":
                    md += f" - {topic['name']}\n"

        return md
