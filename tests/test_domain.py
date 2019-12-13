import pathlib


class TestDomain:
    def test_process_domain(self, lang, greet_intent):
        expected = {
            "slots": [],
            "entities": [],
            "intents": ["greet"],
            "templates": {},
            "actions": [],
        }

        lang.process(greet_intent)

        assert lang.domain == expected

    def test_utter(self, lang):
        utters = """[utter: star-wars]
- O medo leva à raiva, a raiva leva ao ódio e o ódio leva ao sofrimento.
- Que a Força esteja com você!
- Grande guerreiro? Guerra não faz grande ninguém.
- Lembre-se sempre, o seu foco determina a sua realidade.
- Muito a aprender você ainda tem.
"""

        expected = {
            "slots": [],
            "entities": [],
            "intents": [],
            "templates": {
                "utter_star-wars": [
                    {
                        "text": (
                            "O medo leva à raiva, a raiva leva ao ódio"
                            " e o ódio leva ao sofrimento."
                        )
                    },
                    {"text": "Que a Força esteja com você!"},
                    {
                        "text": (
                            "Grande guerreiro?"
                            " Guerra não faz grande ninguém."
                        )
                    },
                    {
                        "text": (
                            "Lembre-se sempre, o seu foco"
                            " determina a sua realidade."
                        )
                    },
                    {"text": "Muito a aprender você ainda tem."},
                ]
            },
            "actions": ["utter_star-wars"],
        }

        lang.process(utters)
        assert lang.domain == expected

    def test_domain_dump(self, lang, starwars_intent, tmpdir):
        lang.domain = {
            "intents": ["star-wars"],
            "actions": [],
            "templates": {},
            "slots": [],
        }

        expected = """intents:
- star-wars
"""

        tmpdir.mkdir("data")
        f = tmpdir.join("domain.yml")

        path = pathlib.Path(tmpdir)
        lang.dump_files(path)

        assert f.read() == expected
