import sys
sys.path.insert(1, '../rasa_language')

from parser import parse


class TestNLU:

    def test_intent(self):
        intent = (
            '[intent: ola]\n'
            '- hello\n'
            '- hi'
        )

        expected = [
            'blocks', [
                'block',
                ['header', ['intent', 'ola']],
                [
                    'list', [
                        ['topic', 'hello'],
                        ['topic', 'hi']
                    ],
                ]
            ],
        ]

        assert parse(intent) == expected
