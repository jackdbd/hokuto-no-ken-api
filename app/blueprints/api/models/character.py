from app.extensions import db
from sqlalchemy.sql.expression import func


class CharacterModel(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, nullable=False)
    name_kanji = db.Column(db.String(16), index=True, nullable=False)
    name_romaji = db.Column(db.String(64), index=True, nullable=False)
    avatar = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(128), nullable=True)
    is_not_in_manga = db.Column(db.Boolean, nullable=False)
    first_appearance_anime = db.Column(db.Integer, nullable=True)
    first_appearance_manga = db.Column(db.Integer, nullable=True)

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
