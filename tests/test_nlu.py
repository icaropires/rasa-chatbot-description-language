import tempfile
import pathlib
import json
from rasa_language import parse, RasaLanguage


class TestNLU:
    def test_parse_intent(self):
        intent = "[intent: greet]\n"
        intent += "> hello\n"
        intent += "> hi\n"

        expected = [
            "blocks",
            [
                "block",
                ["header", "intent", "greet"],
                ["topics", [">", "hello"], [">", "hi"]],
            ],
        ]

        assert parse(intent) == expected

    def test_process_intent(self):
        intent = """[intent: star-wars]
> lado negro da força
> lado negro da forca
> lado negro
> frase de star wars
> guerra nas estrelas
> darth vader
"""

        nlu = {
            "rasa_nlu_data": {
                "common_examples": [
                    {
                        "text": "lado negro da força",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "lado negro da forca",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "lado negro",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "frase de star wars",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "guerra nas estrelas",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "darth vader",
                        "intent": "star-wars",
                        "entities": [],
                    },
                ],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        lang = RasaLanguage()
        lang.process(intent)

        assert lang.nlu == nlu

    def test_nlu_dump(self):
        nlu = {
            "rasa_nlu_data": {
                "common_examples": [
                    {
                        "text": "lado negro da força",
                        "intent": "star-wars",
                        "entities": [],
                    },
                    {
                        "text": "lado negro da forca",
                        "intent": "star-wars",
                        "entities": [],
                    },
                ],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        lang = RasaLanguage()
        lang.nlu = nlu

        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d)

            sub_path = path / "data"
            sub_path.mkdir()

            lang.dump_files(str(path))

            sub_path = sub_path / "nlu.json"
            with open(str(sub_path), "r") as f:
                content = f.read()

                assert content == json.dumps(
                    nlu, ensure_ascii=False, sort_keys=True, indent=4
                )
