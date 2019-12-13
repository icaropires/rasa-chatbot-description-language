import pathlib


class TestDomain:
    def test_process_domain(self, lang, greet_intent):
        expected = {
            "intents": ["greet"],
            "actions": [],
            "templates": {},
            "slots": [],
            "entities": [],
        }

        lang.process(greet_intent)

        assert lang.domain == expected

    def test_utter(
        self, lang,
    ):
        utters = """[utter: star-wars]
- O medo leva à raiva, a raiva leva ao ódio e o ódio leva ao sofrimento.
- Que a Força esteja com você!
- Grande guerreiro? Guerra não faz grande ninguém.
- Lembre-se sempre, o seu foco determina a sua realidade.
- Muito a aprender você ainda tem.
"""

        expected = {
            "intents": [],
            "actions": ["utter_star-wars"],
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
            "slots": [],
            "entities": [],
        }

        lang.process(utters)
        assert lang.domain == expected

    def test_domain_dump(self, lang, starwars_intent, tmpdir):
        lang.domain = {
            "intents": ["star-wars"],
            "actions": [],
            "templates": {},
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
