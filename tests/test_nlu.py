from rasa_language import parse


class TestNLU:
    def test_intent(self):
        intent = "[intent: ola]\n" "- hello\n" "- hi\n"

        expected = [
            "blocks",
            [
                [
                    "block",
                    ["header", ["intent", "ola"]],
                    ["topics", ["hello", "hi"]],
                ]
            ],
        ]

        assert parse(intent) == expected
