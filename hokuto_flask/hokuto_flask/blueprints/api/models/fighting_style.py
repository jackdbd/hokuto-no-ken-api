from sqlalchemy.sql.expression import func
from hokuto_flask.extensions import db
from ..relationships import character_fighting_style_association


class FightingStyleModel(db.Model):
    """Database model for a fighting style in the Hokuto no Ken universe."""

    __tablename__ = "fighting_styles"
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    url = db.Column(db.String(128), nullable=True)
    characters = db.relationship(
        "CharacterModel",
        secondary=character_fighting_style_association,
        back_populates="fighting_styles",
    )

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
