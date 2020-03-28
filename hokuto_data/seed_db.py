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
import mimesis.schema as ms
import sqlite3
from argparse import RawDescriptionHelpFormatter
from dotenv import find_dotenv, load_dotenv

DOTENV_PATH = find_dotenv(".env")
load_dotenv(DOTENV_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))


if os.environ.get("DB_NAME_DEV") is None:
    msg = """DB_NAME_DEV is not set.
    It must be set as an environment variable (you can use a .env file).
    """
    raise KeyError(msg)
else:
    # DB_URI = ":memory:"
    DB_URI = os.path.join(ROOT, os.environ.get("DB_NAME_DEV"))


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
        "first_appearance_anime": _("numbers.integer_number", start=1, end=152),
        "first_appearance_manga": _("numbers.integer_number", start=1, end=999),
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
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    characters = create_fake_characters(args.num_fakes)
    logger.info(f"Generated {len(characters)} fake characters")
    [logger.debug(character) for character in characters]

    with sqlite3.connect(DB_URI) as conn:
        c = conn.cursor()
        tuples = [tuple(d.values()) for d in characters]
        c.executemany("INSERT INTO characters VALUES (?, ?, ?, ?, ?, ?, ?, ?);", tuples)
        c.execute("SELECT * from characters;")
        rows = c.fetchall()
        assert (
            len(rows) == args.num_fakes
        ), f"You generated {args.num_fakes} fakes, but {len(rows)} characters were found in the database."
        print(rows)


if __name__ == "__main__":
    main()
