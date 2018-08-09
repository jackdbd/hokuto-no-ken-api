"""Process scraped items from a Redis queue and populate a database.

Usage:
    $ python updater.py
    # fetch 300 (limit) items from Redis, 20 (batch) at a time
    $ python updater.py -l 300 -b 20
"""
import os
import json
import redis
import logging
import argparse
from redis.exceptions import ConnectionError
from argparse import RawDescriptionHelpFormatter
from dotenv import find_dotenv, load_dotenv, get_key
from sqlalchemy.exc import OperationalError
from db_utils import bulk_insert

# TODO: fix logger
# logger = logging.getLogger("sqlalchemy.engine.base")
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter_str = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

DOTENV_PATH = find_dotenv(".env")
load_dotenv(DOTENV_PATH)

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

REDIS_PORT = get_key(DOTENV_PATH, "REDIS_PORT")
REDIS_HOST = get_key(DOTENV_PATH, "REDIS_HOST")
DB_URI = get_key(DOTENV_PATH, "DB_URI")

ITEMS_KEY = "characters_redis:items"

if not REDIS_HOST:
    raise KeyError("REDIS_HOST environment variable not set.")

if not REDIS_PORT:
    raise KeyError("REDIS_PORT environment variable not set.")

if not DB_URI:
    raise KeyError("DB_URI environment variable not set.")


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="Number of items to fetch from Redis",
    )
    parser.add_argument(
        "-b",
        "--batch",
        type=int,
        default=10,
        help="Batch size (number of items to fetch from Redis at a time)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase verbosity"
    )
    return parser.parse_args()


def fetch_scraped_items(rd, key, i_start, i_stop):
    """

    Parameters
    ----------
    rd : StrictRedis
    key : str
    i_start : int
    i_stop : int

    Returns
    -------
    characters, voice_actors, fighting_styles : list
    """
    redis_items = rd.lrange(key, i_start, i_stop)
    characters = []
    voice_actors = []
    fighting_styles = []
    n_invalid = 0
    for ri in redis_items:
        item = json.loads(ri)
        if item["is_valid"]:
            character = {
                "name_romaji": item["name_romaji"],
                "name_kanji": item["name_kanji"],
                "avatar": item["avatar"],
                "url": item["url"],
                "is_not_in_manga": item["appearances"]["is_not_in_manga"],
                "first_anime_episode": item["appearances"]["first_anime_episode"],
                "first_manga_chapter": item["appearances"]["first_manga_chapter"],
            }
            characters.append(character)

            for voice_actor in item["voice_actors"]:
                voice_actors.append(voice_actor)

            for fighting_style in item["fighting_styles"]:
                fighting_styles.append(fighting_style)
        else:
            n_invalid = n_invalid + 1
            logger.warning(f"Invalid item {item}.")

    n_fetched = i_stop - i_start
    msg = f"{n_fetched} items fetched from Redis ({n_invalid} invalid)."
    logger.debug(msg)
    return characters, voice_actors, fighting_styles


def main():
    # TODO: secure Redis https://redislabs.com/lp/python-redis/
    # TODO: can I obfuscate redis commands with redis-py?
    args = parse_args()
    rd = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    info = rd.connection_pool.get_connection("info")
    try:
        clients = rd.client_list()
    except ConnectionError as e:
        logger.error("Cannot connect to Redis. Was redis-server started?")
        raise e

    logger.debug(f"Connect to Redis on {info.host}:{info.port}")
    logger.debug(f"Clients connected: {clients}")
    assert rd.type(ITEMS_KEY) == b"list"
    num_items = rd.llen(ITEMS_KEY)
    logger.debug(f"{num_items} items in {ITEMS_KEY}")

    # TODO: what's the best way to handle redis fetching + postgres insertions?
    # fetch from redis, try to store in db, then only remove from redis if
    # database write was successful?

    n_processed = 0
    limit = min(args.limit, num_items)
    while n_processed < limit:
        i_start = n_processed
        i_stop = n_processed + args.batch
        characters, voice_actors, fighting_styles = fetch_scraped_items(
            rd, ITEMS_KEY, i_start, i_stop
        )

        # TODO: handle in a transaction for each table?

        try:
            bulk_insert(DB_URI, "characters", characters)
        except OperationalError as e:
            # TODO: if there was an error in writing the database, it's better
            # not to remove the items from the Redis queue and investigate
            logger.error(e)

        try:
            bulk_insert(DB_URI, "voice_actors", voice_actors)
        except OperationalError as e:
            logger.error(e)

        try:
            bulk_insert(DB_URI, "fighting_styles", fighting_styles)
        except OperationalError as e:
            logger.error(e)

        n_processed = n_processed + args.batch
        # rd.lpop() or rd.blpop()?

        print(f"Characters {i_start} - {i_stop}")
        for character in characters:
            print(character)


# engine = sa.create_engine(DB_URI)
# conn = engine.connect()
# result = conn.execute("""SELECT * FROM "characters";""")
# for res in result.fetchall():
#     logger.debug(res)


# print(f"Result: {result.fetchall()}")


# rd.keys()
# rd.scan()
# item = rd.lpop(ITEMS_KEY)
# rd.blpop(ITEMS_KEY)


if __name__ == "__main__":
    main()
