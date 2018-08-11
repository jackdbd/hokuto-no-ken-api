from app.extensions import db
from sqlalchemy.sql.expression import func


class VoiceActorModel(db.Model):
    """Database model for a voice actor (seiyū) in the Hokuto no Ken universe.

    It seems that the voice actor's name is unique on Hokuto Renkitōza. If not,
    this would be problematic (see documentation in models/character).
    """
    __tablename__ = "voice_actors"
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    url = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.name}>"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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
