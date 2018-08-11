"""Models for the API blueprint.

A model is the INTERNAL representation of an entity.
"""
from .character import CharacterModel
from .voice_actor import VoiceActorModel
from .fighting_style import FightingStyleModel
from .relationships import character_voice_actor_association_table
