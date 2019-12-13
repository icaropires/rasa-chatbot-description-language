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
    def test_parse_intent(self, greet_intent):
        expected = [
            "blocks",
            [
                "block",
                ["header", "intent", "greet"],
                ["topics", [">", ["text", "hello"]], [">", ["text", "hi"]]],
            ],
        ]

        assert parse(greet_intent) == expected

    def test_process_intent(self, lang, starwars_intent, starwars_intent_nlu):
        lang.process(starwars_intent)

        assert lang.nlu == starwars_intent_nlu

    def test_nlu_dump(
        self, lang, starwars_intent, starwars_intent_nlu, tmpdir
    ):
        lang.nlu = starwars_intent_nlu

        f = tmpdir.mkdir("data").join("nlu.json")

        path = pathlib.Path(tmpdir)
        lang.dump_files(path)

        assert f.read() == json.dumps(
            starwars_intent_nlu, ensure_ascii=False, sort_keys=True, indent=4,
        )
