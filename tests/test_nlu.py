from rasa_language import parse


class TestNLU:
    def test_intent(self):
        intent = "[intent: greet]\n"
        intent += "> hello\n"
        intent += "> hi\n"

        expected = [
            "blocks",
            [
                [
                    "block",
                    ["header", ["intent", "greet"]],
                    ["topics", [">", "hello"], [">", "hi"]],
                ]
            ],
        ]

        assert parse(intent) == expected
