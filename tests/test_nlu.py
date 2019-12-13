import tempfile
import pathlib
import json

import pytest
from rasa_language import parse


@pytest.fixture
def starwars_intent_nlu():
    return {
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
                {"text": "lado negro", "intent": "star-wars", "entities": []},
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


class TestNLU:
    def test_parse_intent(self):
        intent = """[intent: greet]
> hello
> hi
"""

        expected = [
            "blocks",
            [
                "block",
                ["header", "intent", "greet"],
                ["topics", [">", "hello"], [">", "hi"]],
            ],
        ]

        assert parse(intent) == expected

    def test_process_intent(self, lang, starwars_intent, starwars_intent_nlu):
        lang.process(starwars_intent)

        assert lang.nlu == starwars_intent_nlu

    def test_nlu_dump(self, lang, starwars_intent, starwars_intent_nlu):
        lang.nlu = starwars_intent_nlu

        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d)

            sub_path = path / "data"
            sub_path.mkdir()

            lang.dump_files(str(path))

            sub_path = sub_path / "nlu.json"
            with open(str(sub_path), "r") as f:
                content = f.read()

                assert content == json.dumps(
                    starwars_intent_nlu,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
