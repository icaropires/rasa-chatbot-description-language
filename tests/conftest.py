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
def starwars_intent():
    return """[intent: star-wars]
> lado negro da força
> lado negro da forca
> lado negro
> frase de star wars
> guerra nas estrelas
> darth vader
"""
