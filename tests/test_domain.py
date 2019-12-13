import pathlib


class TestDomain:
    def test_process_domain(self, lang, greet_intent):
        expected = {
            "intents": ["greet"],
            "actions": [],
            "templates": [],
            "slots": [],
            "entities": [],
        }

        lang.process(greet_intent)

        assert lang.domain == expected

    def test_domain_dump(self, lang, starwars_intent, tmpdir):
        lang.domain = {
            "intents": ["star-wars"],
            "actions": [],
            "templates": [],
            "slots": [],
            "entities": [],
        }

        expected = """intents:
- star-wars
"""

        tmpdir.mkdir("data")
        f = tmpdir.join("domain.yml")

        path = pathlib.Path(tmpdir)
        lang.dump_files(path)

        assert f.read() == expected
