import pathlib


class TestStories:
    def test_stories_process(self, lang):
        story = """[star-wars]
> Quero conselhos do yoda
- O medo é o caminho para o lado negro.

[intent: star-wars]
> Quero conselhos do yoda
> Eu gostaria de conselhos do mestre

[utter: star-wars]
- O medo é o caminho para o lado negro.
- Que a Força esteja com você!
"""
        expected = {
            "star-wars": [
                {"type": "intent", "name": "star-wars", "entities": {}},
                {"type": "action", "name": "utter_star-wars"},
            ]
        }

        lang.process(story)

        assert lang.stories == expected

    def test_stories_dump(self, lang, tmpdir):
        lang.stories = {
            "Star Wars": [
                {"type": "intent", "name": "greet", "entities": {}},
                {"type": "action", "name": "utter_answer_hi"},
                {
                    "type": "intent",
                    "name": "fight",
                    "entities": {"saber": "red", "philosophy": "sith"},
                },
                {"type": "action", "name": "utter_easy"},
                {"type": "action", "name": "utter_bye"},
            ]
        }

        expected = """## Star Wars
* greet
 - utter_answer_hi
* fight{"saber": "red", "philosophy": "sith"}
 - utter_easy
 - utter_bye
"""

        f = tmpdir.mkdir("data").join("stories.md")

        path = pathlib.Path(tmpdir)
        lang.dump_files(path)

        assert f.read() == expected
