import os
import logging
import requests
import lxml.html
import sqlalchemy as sa
from characters import scrape_characters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqlalchemy.engine.base")
logger.setLevel(logging.DEBUG)

BASE_URL = "http://hokuto.wikia.com"
CHARACTERS_URL = f"{BASE_URL}/wiki/List_of_Hokuto_no_Ken_characters"


def create_characters_table(db_uri):
    engine = sa.create_engine(db_uri)
    metadata = sa.MetaData()
    characters = sa.Table(
        "characters",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(25), nullable=False),
        sa.Column("url", sa.String(25), nullable=True),
        sa.Column("is_not_in_manga", sa.Boolean, nullable=False),
    )
    logger.debug(metadata.tables)

    # Store in the DB the schema we have just defined
    metadata.create_all(engine)
    return characters


def scrape_and_store(html, db_uri, table):
    root = lxml.html.fromstring(html)
    characters_not_in_manga = scrape_characters(
        root, "div#mw-content-text > ul > li > i > a", True
    )
    characters_in_manga = scrape_characters(
        root, "div#mw-content-text > ul > li > a", False
    )
    engine = sa.create_engine(db_uri)
    conn = engine.connect()
    clause = table.insert()
    conn.execute(clause, characters_not_in_manga)
    conn.execute(clause, characters_in_manga)
    return None


if __name__ == "__main__":
    DB_PATH = "data.db"
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)
    db_uri = f"sqlite:///{DB_PATH}"
    characters = create_characters_table(db_uri)
    req = requests.get(CHARACTERS_URL)
    scrape_and_store(req.text, db_uri, characters)

    # Of course we can also use raw SQL to fetch all the results
    engine = sa.create_engine(db_uri)
    conn = engine.connect()
    result = conn.execute(
        """
        SELECT c.name FROM characters as c
        WHERE c.is_not_in_manga = 1 
        ORDER BY c.name DESC
        LIMIT 3;
        """
    )
    print(f"Result: {result.fetchall()}")
