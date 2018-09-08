"""Seed a database with some fakes.

Usage:
    $ python seed_db.py
    $ python seed_db.py -n 100 -v

See Also
    The table names can be found in the Flask app DB models and relationships.
"""
import os
import logging
import argparse
import sqlalchemy as sa
import sqlalchemy.orm as orm
import mimesis.schema as ms
from argparse import RawDescriptionHelpFormatter
from sqlalchemy.ext.declarative import declarative_base
from db_utils import get_table


# Log SQLAlchemy operations
logger_sa = logging.getLogger("sqlalchemy.engine.base")

DB_URI = f"sqlite:///:memory:"
Base = declarative_base()
Session = orm.sessionmaker()


# TODO: how to get the database schema? Via Reflection?
class Character(Base):
    __tablename__ = "characters"
    id = sa.Column(sa.String(32), primary_key=True, autoincrement=False)
    name = sa.Column(sa.String(32), index=True, unique=True, nullable=False)
    name_kanji = sa.Column(sa.String(16), index=True, unique=False, nullable=False)
    name_romaji = sa.Column(sa.String(64), index=True, unique=False, nullable=False)
    avatar = sa.Column(sa.String(128), nullable=True)
    url = sa.Column(sa.String(128), nullable=True)
    first_appearance_anime = sa.Column(sa.Integer, nullable=True)
    first_appearance_manga = sa.Column(sa.Integer, nullable=True)


def make_character(seed):
    _ = ms.Field(locale="en", seed=seed)
    ja = ms.Field(locale="ja", seed=seed)
    description = lambda: {
        "id": _("uuid"),
        "name": _("person.full_name"),
        "name_kanji": ja("person.full_name"),
        "name_romaji": _("person.full_name"),
        "avatar": _("person.avatar"),
        "url": _("internet.home_page"),
        "first_appearance_anime": _("numbers.between", minimum=1, maximum=152),
        "first_appearance_manga": _("numbers.between", minimum=1, maximum=999),
    }
    schema = ms.Schema(schema=description)
    character = schema.create(iterations=1)[0]
    return character


def create_fake_characters(num_characters):
    characters = [make_character(i) for i in range(num_characters)]
    return characters


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-n", "--num_fakes", default=10, type=int, help="Num. of fakes to create"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase output verbosity"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logger_sa.setLevel(logging.DEBUG)
    else:
        logger_sa.setLevel(logging.WARNING)

    engine = sa.create_engine(DB_URI)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    conn = engine.connect()

    characters = create_fake_characters(args.num_fakes)
    table = get_table(engine, "characters")
    clause = table.insert()
    conn.execute(clause, characters)

    sql = """
    SELECT * from "characters";
    """
    results = conn.execute(sql)
    rows = results.fetchall()
    assert len(rows) == args.num_fakes
    # print(rows)


if __name__ == "__main__":
    main()
