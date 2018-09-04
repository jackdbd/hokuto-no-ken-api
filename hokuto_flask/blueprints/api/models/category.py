from sqlalchemy.sql.expression import func
from hokuto_flask.extensions import db
from ..relationships import character_category_association


class CategoryModel(db.Model):
    """Database model for a category in the Hokuto no Ken universe.
    """

    __tablename__ = "categories"
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    url = db.Column(db.String(128), nullable=True)
    characters = db.relationship(
        "CharacterModel",
        secondary=character_category_association,
        back_populates="categories",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.name}>"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def random(cls):
        return cls.query.order_by(func.random()).first()
