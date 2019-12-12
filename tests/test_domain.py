from rasa_language import RasaLanguage


class TestDomain:
    def test_parse_domain(self):
        intent = """[intent: greet]
> hello
> hi
"""
        print("@@@@@@@@@@@@@@@@@@")
        print(intent)
        print("@@@@@@@@@@@@@@@@@@")

        exptected = {
            "intents": ["greet"],
            "actions": [],
            "templates": [],
            "slots": [],
            "entities": [],
        }

        lang = RasaLanguage()
        lang.process(intent)

        assert lang.domain == exptected
