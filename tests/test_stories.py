import pathlib


class TestStories:
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

        tmpdir.mkdir("data")
        f = tmpdir.join("stories.md")

        path = pathlib.Path(tmpdir)
        lang.dump_files(path)

        assert f.read() == expected
