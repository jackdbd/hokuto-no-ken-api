from app.extensions import db
from sqlalchemy.sql.expression import func


class VoiceActorModel(db.Model):
    __tablename__ = "voice_actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(32), nullable=True)

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
