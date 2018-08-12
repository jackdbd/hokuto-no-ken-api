"""Process scraped items from a Redis queue and populate a database.

Don't forget to start the redis server with `redis-server`.
During development, it might be useful to connect to the redis server with the
redis native client. Launch it with `redis-cli`

Usage:
    $ python process_items.py
    # fetch 300 (limit) items from Redis, 20 (batch) at a time, verbose output
    $ python process_items.py -l 300 -b 20 -v
    # fetch all items from Redis, 50 at a time (default batch), delete all
    # records from all tables in the database
    $ python process_items.py -d
"""
import os
import copy
import json
import redis
import logging
import argparse
import sqlalchemy as sa
from redis.exceptions import ConnectionError
from hashlib import md5
from argparse import RawDescriptionHelpFormatter
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.exc import OperationalError, IntegrityError
from db_utils import alembic_revision, delete_all, get_table


# TODO: add flag to cleanup the redis queue
# TODO: add flag to drop all data from the db tables (or maybe drop all the
# database and re-run migrations)


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
ENV = os.environ.get("ENV")


if ENV == "dev":
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_HOST = os.environ["REDIS_HOST_DEV"]
    # DB_URI = f"sqlite:///{HERE}/{os.environ['DB_NAME_DEV']}"
    DB_URI = os.environ.get("DB_URI_PROD")
    REDIS_ITEMS_KEY = os.environ["REDIS_CHARACTERS_KEY"]
elif ENV == "prod":
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_HOST = os.environ["REDIS_HOST_PROD"]
    DB_URI = os.environ["DB_URI_PROD"]
    REDIS_ITEMS_KEY = os.environ["REDIS_CHARACTERS_KEY"]
else:
    msg = f"Cannot run in a {ENV} environment"
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
        "-d",
        "--delete",
        action="store_true",
        help="If set, delete all records from all database tables before"
        "processing data from Redis",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase output verbosity"
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


def assign_ids(item, keys):

    def assign_id(d):
        id_ = md5(d["name"].encode("utf-8")).hexdigest()
        d_ = {"id": id_, **d}
        return d_

    scraped_data = copy.deepcopy(item["scraped_data"])
    for k in keys:
        if isinstance(scraped_data[k], dict):
            scraped_data[k] = assign_id(scraped_data[k])
        else:
            scraped_data[k] = [assign_id(d) for d in scraped_data[k]]

    item_with_ids = {**item, "scraped_data": scraped_data}
    return item_with_ids


def sanitize(item):
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
    sanitized = {
        "character": character,
        "categories": categories,
        "voice_actors": voice_actors,
        "fighting_styles": fighting_styles,
        "family_members": family_members,
        "allegiances": allegiances,
    }
    scraped_data = {**d, **sanitized}
    item_sanitized = {**item, "scraped_data": scraped_data}
    return item_sanitized


def extract_data(redis_items):
    """Extract data from the web-scraped items found in Redis.

    Parameters
    ----------
    redis_items : list
        scraped items from the Redis queu. Each item was serialized by the
        scrapy_redis RedisPipeline.

    Returns
    -------
    data : list
        entries sanitized and normalized, so they can be sent to the database.
        Note that there might be duplicates. This must be handled later, when
        trying to insert each datum into the respective table.
    """
    data = []
    n_invalid = 0
    for ri in redis_items:
        item = json.loads(ri)
        if item["scraped_data"] is None:
            logger.warning(f"{item['url']} does not contain scraped data.")
            n_invalid = n_invalid + 1
        else:
            if is_valid(item):
                # sanitize first, then assign ids
                item_sanitized = sanitize(item)
                # find these keys in the item dict and assign an id to each one
                keys = (
                    "character",
                    "categories",
                    "voice_actors",
                    "fighting_styles",
                    "family_members",
                    "allegiances",
                )
                item_with_ids = assign_ids(item_sanitized, keys)

                character = item_with_ids["scraped_data"]["character"]
                data.append({"table": "characters", "datum": character})

                table_names = (
                    "categories",
                    "voice_actors",
                    "fighting_styles",
                    "family_members",
                    "allegiances",
                )
                for table_name in table_names:
                    for datum in item_with_ids["scraped_data"][table_name]:
                        data.append({"table": table_name, "datum": datum})

                for va in item_with_ids["scraped_data"]["voice_actors"]:
                    datum = {
                        "character_id": character["id"], "voice_actor_id": va["id"]
                    }
                    data.append({"table": "characters_voice_actors", "datum": datum})
            else:
                n_invalid = n_invalid + 1
                logger.warning(f"{item['url']} contains invalid scraped data.")

    logger.debug(f"{len(redis_items)} items from Redis --> {len(data)} data.")
    return data


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
    logger.info(f"{num_items} items in {REDIS_ITEMS_KEY}")

    # TODO: what's the best way to handle redis fetching + postgres insertions?
    # fetch from redis, try to store in db, then only remove from redis if
    # database write was successful?

    engine = sa.create_engine(DB_URI)
    conn = engine.connect()
    db_revision = alembic_revision(conn)
    logger.info(f"Database version: {db_revision}")

    if args.delete:
        delete_all(engine, "characters_voice_actors")
        delete_all(engine, "characters_categories")
        delete_all(engine, "characters")
        delete_all(engine, "voice_actors")
        delete_all(engine, "fighting_styles")
        delete_all(engine, "categories")

    if args.limit is None:
        limit = num_items
    else:
        limit = int(args.limit)

    i0 = 0
    while i0 <= limit:
        i1 = min(limit - 1, i0 + args.batch - 1)
        logger.info(f"Processing items [{i0} - {i1}]")
        redis_items = rd.lrange(REDIS_ITEMS_KEY, i0, i1)
        logger.debug(f"{len(redis_items)} items found in Redis.")
        data = extract_data(redis_items)

        # TODO: if there was an error in writing the database, it's better not
        # to remove the items from the Redis queue and investigate

        table_names = ("characters", "voice_actors", "fighting_styles", "categories")
        for table_name in table_names:
            table_data = [d["datum"] for d in data if d["table"] == table_name]
            if table_data:
                table = get_table(engine, table_name)
                clause = table.insert()
                try:
                    conn.execute(clause, data)
                except IntegrityError as e:
                    e.add_detail("Bulk insert failed. Insert one-by-one.")
                    logger.error(e)
                    for datum in table_data:
                        try:
                            conn.execute(clause, datum)
                        except IntegrityError as e:
                            logger.error(e)
                except OperationalError as e:
                    e.add_detail("FIXME")
                    logger.critical(e)

        association_table_names = ("characters_voice_actors", "characters_categories")
        for table_name in association_table_names:
            table_data = [d["datum"] for d in data if d["table"] == table_name]
            if table_data:
                table = get_table(engine, table_name)
                clause = table.insert()
                try:
                    logger.debug(f"Try Bulk insert of {len(data)} records.")
                    conn.execute(clause, data)
                except IntegrityError as e:
                    e.add_detail("Bulk insert failed. Insert one-by-one.")
                    logger.error(e)
                    for datum in table_data:
                        try:
                            conn.execute(clause, datum)
                        except IntegrityError as e:
                            logger.error(e)
                except OperationalError as e:
                    e.add_detail("FIXME")
                    logger.critical(e)

        i0 = i0 + args.batch


# rd.lpop() or rd.blpop()?
# rd.keys()
# rd.scan()
# item = rd.lpop(ITEMS_KEY)
# rd.blpop(ITEMS_KEY)


if __name__ == "__main__":
    main()
