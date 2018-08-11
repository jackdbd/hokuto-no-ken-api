from app.extensions import db


# characters - voice_actors (many to many relationship)
character_voice_actor_association_table = db.Table(
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
)
