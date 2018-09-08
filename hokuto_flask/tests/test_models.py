import pytest
from hokuto_flask.blueprints.api.models import CharacterModel
from .factories import make_character


@pytest.mark.usefixtures("db_empty")
class TestCharacterDbEmpty:
    def test_find_by_id(self):
        d = make_character(seed=42)
        character = CharacterModel(**d)
        character.save()
        retrieved = CharacterModel.find_by_id(character.id)
        assert retrieved == character

    def test_find_by_name(self):
        d = make_character(seed=42)
        character = CharacterModel(**d)
        character.save()
        retrieved = CharacterModel.find_by_name(character.name_romaji)
        assert retrieved == character
        assert character.name_romaji == retrieved.name_romaji

    def test_random(self):
        characters = []
        for i in range(3):
            d = make_character(seed=i)
            character = CharacterModel(**d)
            character.save()
            characters.append(character)
        retrieved = CharacterModel.random()
        assert retrieved in characters


@pytest.mark.usefixtures("db_full")
class TestCharacterDbFull:
    def test_random(self):
        retrieved = CharacterModel.random()
        assert isinstance(retrieved, CharacterModel)
