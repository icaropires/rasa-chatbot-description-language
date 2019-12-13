import json
import yaml
import click
import pathlib
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

        self.domain = {
            "intents": [],
            "actions": [],
            "templates": [],
            "slots": [],
            "entities": [],
        }

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
            header, *topics = args

            type_, name = self.eval(header)
            topics = self.eval(*topics)

            if type_ == "intent":
                c_examples = [
                    {"text": topic, "intent": name, "entities": []}
                    for _, topic in topics
                ]

                self.nlu["rasa_nlu_data"]["common_examples"].extend(c_examples)
                self.domain["intents"].append(name)

        elif head == "header":
            type_, name = args
            return type_, name

        elif head == "topics":
            topics = args
            return topics

        else:
            raise ValueError(f"Unexpected type on syntax tree: {head}")

    def dump_files(self, bot_dir):
        self._dump_nlu(bot_dir)
        self._echo_succesfully_dumped("NLU")

        self._dump_stories(bot_dir)
        # self._echo_succesfully_dumped('Stories')

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
            f.write(yaml.dump(self.domain, default_flow_style=False))

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
