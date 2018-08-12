"""Relationships between models.

These are DATABASE relationships. They create new tables in the database,
include columns which are foreign keys, and might include unique constraints
resulting from a combination of multiple foreign keys. For instance, there
cannot be duplicates for a pair of [character - voice actor], so this
combination is unique.

These database relationships can be used in a model to define relationships at
the OBJECT level. For instance, in the CharacterModel we can define a
relationship with the VoiceActorModel with this syntax:

voice_actors = db.relationship(
    "VoiceActorModel",
    secondary=character_voice_actor_association,
    back_populates="characters",
)

Notes
    I prefer to use back_populates to backref. I find it more explicit.

See Also
    http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    http://docs.sqlalchemy.org/en/latest/core/constraints.html
"""
from hokuto_flask.extensions import db


# characters - voice_actors (many to many)
character_voice_actor_association = db.Table(
    "characters_voice_actors",
    db.Model.metadata,
    db.Column(
        "character_id", db.String(32), db.ForeignKey("characters.id"), nullable=False
    ),
    db.Column(
        "voice_actor_id",
        db.String(32),
        db.ForeignKey("voice_actors.id"),
        nullable=False,
    ),
    db.UniqueConstraint(
        "character_id", "voice_actor_id", name="character_id_voice_actor_id"
    ),
)

# characters - categories (many to many)
character_category_association = db.Table(
    "characters_categories",
    db.Model.metadata,
    db.Column(
        "character_id", db.String(32), db.ForeignKey("characters.id"), nullable=False
    ),
    db.Column(
        "category_id", db.String(32), db.ForeignKey("categories.id"), nullable=False
    ),
    db.UniqueConstraint("character_id", "category_id", name="character_id_category_id"),
)
