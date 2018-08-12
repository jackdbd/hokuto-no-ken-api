from sqlalchemy.sql.expression import func
from hokuto_flask.extensions import db
from ..relationships import character_voice_actor_association, character_category_association


class CharacterModel(db.Model):
    """Database model for a character in the Hokuto no Ken universe.

    A few considerations.

    We cannot use autoincrement=True to generate an ID. We need a ID which
    stays the same every time we scrape Hokuto Renkitōza. E.g. if one day we
    scrape only Kenshiro, Kenshiro gets assigned ID = 1. If another day we
    scrape Kaioh and Kenshiro, Kenshiro gets assigned ID = 2. The only thing
    which seems unique across all scraped pages is the character's name.

    name seems unique and always available when the spider was successful.
    name_kanji and name_romaji might not be available and are not unique (e.g.
    a few characters have the same name_kanji)

    url can be NULL because a character might be listed in the wiki, but there
    is not (yet) an associated character's page.
    """
    __tablename__ = "characters"
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    name_kanji = db.Column(db.String(16), index=True, unique=False, nullable=False)
    name_romaji = db.Column(db.String(64), index=True, unique=False, nullable=False)
    avatar = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(128), nullable=True)
    first_appearance_anime = db.Column(db.Integer, nullable=True)
    first_appearance_manga = db.Column(db.Integer, nullable=True)
    voice_actors = db.relationship(
        "VoiceActorModel",
        secondary=character_voice_actor_association,
        back_populates="characters",
    )
    categories = db.relationship(
        "CategoryModel",
        secondary=character_category_association,
        back_populates="characters",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.name_romaji} ({self.name_kanji})>"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name_romaji):
        return cls.query.filter_by(name_romaji=name_romaji).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def random(cls):
        return cls.query.order_by(func.random()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_in_db(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
