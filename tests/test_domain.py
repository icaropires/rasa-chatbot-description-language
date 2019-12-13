class TestDomain:
    def test_parse_domain(self, lang, greet_intent):
        exptected = {
            "intents": ["greet"],
            "actions": [],
            "templates": [],
            "slots": [],
            "entities": [],
        }

        lang.process(greet_intent)

        assert lang.domain == exptected
