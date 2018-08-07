import os
import logging
import requests
import itertools
import lxml.html
import sqlalchemy as sa
from db_utils import DB_PATH, DB_URI, create_characters_table
from characters import scrape_characters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqlalchemy.engine.base")
logger.setLevel(logging.DEBUG)

BASE_URL = "http://hokuto.wikia.com"
CHARACTERS_URL = f"{BASE_URL}/wiki/List_of_Hokuto_no_Ken_characters"


def scrape(html):
    root = lxml.html.fromstring(html)
    characters_not_in_manga = scrape_characters(
        root, "div#mw-content-text > ul > li > i > a", True
    )
    characters_in_manga = scrape_characters(
        root, "div#mw-content-text > ul > li > a", False
    )
    kenshiro = scrape_characters(root, "div#mw-content-text > ul > li > b > a", False)
    nested = [characters_not_in_manga, characters_in_manga, kenshiro]
    characters = list(itertools.chain(*nested))
    return characters


def store(conn, table, data):
    clause = table.insert()
    conn.execute(clause, data)


def retrieve(conn):
    result = conn.execute(
        """
        SELECT c.name_romaji FROM characters as c
        WHERE c.is_not_in_manga = 1 
        ORDER BY c.name_romaji DESC
        LIMIT 3;
        """
    )
    print(f"Result: {result.fetchall()}")


def main():
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)
    engine = sa.create_engine(DB_URI)
    characters_table = create_characters_table(engine)
    req = requests.get(CHARACTERS_URL)
    characters = scrape(req.text)
    conn = engine.connect()
    store(conn, characters_table, characters)
    retrieve(conn)


if __name__ == "__main__":
    main()
