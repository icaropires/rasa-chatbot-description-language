from rasa_language import parse, Runtime


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

    def test_run_intent(self):
        intent = """[intent: star-wars]
> lado negro da força
> lado negro da forca
> lado negro
> frase de star wars
> guerra nas estrelas
> darth vader
"""

        nlu_json = {
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

        runtime = Runtime()
        assert runtime.eval(parse(intent)) == nlu_json
