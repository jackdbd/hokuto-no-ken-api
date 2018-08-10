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
from dotenv import find_dotenv, load_dotenv
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


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

if "DYNO" in os.environ:
    print("the app is on Heroku")
else:
    DOTENV_PATH = find_dotenv(".env")
    load_dotenv(DOTENV_PATH)

REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_HOST = os.environ["REDIS_HOST"]
DB_URI = os.environ["DB_URI"]
REDIS_ITEMS_KEY = os.environ["REDIS_CHARACTERS_KEY"]


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


def is_valid(d):
    boolean = all(
        [
            v is not None
            for k, v in d.items()
            if k in ("name", "name_kanji", "name_romaji")
        ]
    )
    return boolean


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
    categories = []
    voice_actors = []
    fighting_styles = []
    family_members = []
    allegiances = []
    n_invalid = 0
    for ri in redis_items:
        item = json.loads(ri)
        if item["scraped_data"] is None:
            logger.debug(
                f"{item['url']} does not contain scraped data. Check the page and your spiders."
            )
            n_invalid = n_invalid + 1
        else:
            d = item["scraped_data"]
            if is_valid(d):
                character = {
                    "name": d["name"],
                    "name_romaji": d["name_romaji"],
                    "name_kanji": d["name_kanji"],
                    "avatar": d["avatar"],
                    "first_appearance_anime": d["first_appearance"]["anime"],
                    "first_appearance_manga": d["first_appearance"]["manga"],
                }
                characters.append(character)

                for category in d["categories"]:
                    categories.append(category)

                for voice_actor in d["voice_actors"]:
                    voice_actors.append(voice_actor)

                for fighting_style in d["fighting_styles"]:
                    fighting_styles.append(fighting_style)

                for family_member in d["family_members"]:
                    family_members.append(family_member)

                for allegiance in d["allegiances"]:
                    allegiances.append(allegiance)
            else:
                n_invalid = n_invalid + 1
                logger.debug(
                    f"{item['url']} contains invalid scraped data. Check the page and your spiders."
                )

    n_fetched = i_stop - i_start
    msg = f"{n_fetched} items fetched from Redis ({n_invalid} invalid)."
    logger.debug(msg)
    return characters, categories, voice_actors, fighting_styles, family_members, allegiances


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
    assert rd.type(REDIS_ITEMS_KEY) == b"list"
    num_items = rd.llen(REDIS_ITEMS_KEY)
    logger.debug(f"{num_items} items in {REDIS_ITEMS_KEY}")

    # TODO: what's the best way to handle redis fetching + postgres insertions?
    # fetch from redis, try to store in db, then only remove from redis if
    # database write was successful?

    n_processed = 0
    limit = min(args.limit, num_items)
    while n_processed < limit:
        i_start = n_processed
        i_stop = n_processed + args.batch
        characters, categories, voice_actors, fighting_styles, family_members, allegiances = fetch_scraped_items(
            rd, REDIS_ITEMS_KEY, i_start, i_stop
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
