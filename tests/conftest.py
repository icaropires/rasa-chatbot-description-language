import pytest
from rasa_language import RasaLanguage


@pytest.fixture
def lang():
    return RasaLanguage()


@pytest.fixture
def greet_intent():
    return """[intent: greet]
> hello
> hi
"""


@pytest.fixture
def programming_lang_intent():
    return (
        "[intent: programming]\n"
        "> Você gosta de programar em {JS}{lang:java|php|javascript|"
        "haskell|python|c|c++|c#}?\n"
    )


@pytest.fixture
def starwars_intent():
    return """[intent: star-wars]
> lado negro da força
> lado negro da forca
> lado negro
> frase de star wars
> guerra nas estrelas
> darth vader
"""
