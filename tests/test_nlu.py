from rasa_language import parse


class TestNLU:
    def test_intent(self):
        intent = "[intent: ola]\n" "- hello\n" "- hi"

        expected = [
            "blocks",
            [
                [
                    ["header", ["intent", "ola"]],
                    ["topics", [["topic", "hello"], ["topic", "hi"]]],
                ]
            ],
        ]

        assert parse(intent) == expected
