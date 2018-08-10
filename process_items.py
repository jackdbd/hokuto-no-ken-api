"""Process scraped items from a Redis queue and populate a database.

Usage:
    $ python process_items.py
    # fetch 300 (limit) items from Redis, 20 (batch) at a time, verbose
    $ python process_items.py -l 300 -b 20 -v
"""
import os
import json
import redis
import logging
import argparse
from redis.exceptions import ConnectionError
from argparse import RawDescriptionHelpFormatter
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.exc import OperationalError, IntegrityError
from db_utils import bulk_insert, alembic_revision


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)

ch = logging.StreamHandler()

fh = logging.FileHandler("process_items.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

DOTENV_PATH = find_dotenv(".env")
load_dotenv(DOTENV_PATH)

if os.environ["ENVIRONMENT"] == "dev":
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_HOST = os.environ["REDIS_HOST_DEV"]
    DB_URI = f"sqlite:///{HERE}/{os.environ['DB_NAME_DEV']}"
    REDIS_ITEMS_KEY = os.environ["REDIS_CHARACTERS_KEY"]
elif os.environ["ENVIRONMENT"] == "prod":
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_HOST = os.environ["REDIS_HOST_PROD"]
    DB_URI = os.environ["DB_URI_PROD"]
    REDIS_ITEMS_KEY = os.environ["REDIS_CHARACTERS_KEY"]
else:
    msg = f"Cannot run in a {os.environ['ENVIRONMENT']} environment"
    raise KeyError(msg)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=None,
        help="Num. of items to fetch from Redis (default: None -> fetch all)",
    )
    parser.add_argument(
        "-b",
        "--batch",
        type=int,
        default=50,
        help="Num. of items to fetch from Redis at a time (default: 50)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase verbosity"
    )
    return parser.parse_args()


def is_valid(item):
    if item.get("scraped_data") is None:
        boolean = False
    else:
        d = item["scraped_data"]
        boolean = all(
            [
                v is not None
                for k, v in d.items()
                if k in ("name", "name_kanji", "name_romaji")
            ]
        )
    return boolean


def sanitize_scraped_data(item):
    d = item["scraped_data"]
    avatar = d["avatar"] if d.get("avatar") else None

    if d.get("first_appearance"):
        first_appearance_anime = d["first_appearance"]["anime"]
        first_appearance_manga = d["first_appearance"]["manga"]
    else:
        first_appearance_anime = None
        first_appearance_manga = None

    character = {
        "name": d["name"],
        "name_romaji": d["name_romaji"],
        "name_kanji": d["name_kanji"],
        "url": item["url"],
        "avatar": avatar,
        "first_appearance_anime": first_appearance_anime,
        "first_appearance_manga": first_appearance_manga,
    }
    categories = d["categories"] if d.get("categories") else []
    voice_actors = d["voice_actors"] if d.get("voice_actors") else []
    fighting_styles = d["fighting_styles"] if d.get("fighting_styles") else []
    family_members = d["family_members"] if d.get("family_members") else []
    allegiances = d["allegiances"] if d.get("allegiances") else []
    d_ = {
        "character": character,
        "categories": categories,
        "voice_actors": voice_actors,
        "fighting_styles": fighting_styles,
        "family_members": family_members,
        "allegiances": allegiances,
    }
    return d_


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
            logger.warning(f"{item['url']} does not contain scraped data.")
            n_invalid = n_invalid + 1
        else:
            if is_valid(item):
                d_ = sanitize_scraped_data(item)
                characters.append(d_["character"])

                for category in d_["categories"]:
                    categories.append(category)

                for voice_actor in d_["voice_actors"]:
                    voice_actors.append(voice_actor)

                for fighting_style in d_["fighting_styles"]:
                    fighting_styles.append(fighting_style)

                for family_member in d_["family_members"]:
                    family_members.append(family_member)

                for allegiance in d_["allegiances"]:
                    allegiances.append(allegiance)
            else:
                n_invalid = n_invalid + 1
                logger.warning(f"{item['url']} contains invalid scraped data.")

    n_fetched = i_stop - i_start
    logger.info(f"{n_fetched} items fetched from Redis ({n_invalid} invalid).")
    return characters, categories, voice_actors, fighting_styles, family_members, allegiances


def main():
    # TODO: secure Redis https://redislabs.com/lp/python-redis/
    # TODO: can I obfuscate redis commands with redis-py?
    args = parse_args()
    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

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

    db_revision = alembic_revision(DB_URI)

    n_processed = 0
    if args.limit is None:
        limit = num_items
    else:
        limit = int(args.limit)
    while n_processed < limit:
        i_start = n_processed
        i_stop = n_processed + args.batch
        logger.info(f"Processing items [{i_start} - {i_stop}]")
        characters, categories, voice_actors, fighting_styles, family_members, allegiances = fetch_scraped_items(
            rd, REDIS_ITEMS_KEY, i_start, i_stop
        )

        # TODO: handle in a transaction for each table?

        # TODO: if there was an error in writing the database, it's better not
        # to remove the items from the Redis queue and investigate

        if characters:
            bulk_insert(DB_URI, "characters", characters)
        # try:
        #     bulk_insert(DB_URI, "characters", characters)
        # except OperationalError as e:
        #     logger.error(e)
        # except IntegrityError as e:
        #     logger.error(e)

        if voice_actors:
            bulk_insert(DB_URI, "voice_actors", voice_actors)
        # try:
        #     bulk_insert(DB_URI, "voice_actors", voice_actors)
        # except OperationalError as e:
        #     logger.error(e)
        # except IntegrityError as e:
        #     logger.error(e)

        if fighting_styles:
            bulk_insert(DB_URI, "fighting_styles", fighting_styles)
        # try:
        #     bulk_insert(DB_URI, "fighting_styles", fighting_styles)
        # except OperationalError as e:
        #     logger.error(e)
        # except IntegrityError as e:
        #     logger.error(e)

        n_processed = n_processed + args.batch


# rd.lpop() or rd.blpop()?

# print(f"Characters {i_start} - {i_stop}")
# for character in characters:
#     print(character)


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
