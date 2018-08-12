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

See Also
    The table names can be found in the Flask app DB models and relationships.
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

# item key in Redis --> DB table
MAPPINGS_MODEL_TABLES = (
    {"item_key": "character", "table": "characters"},
    {"item_key": "voice_actors", "table": "voice_actors"},
    {"item_key": "fighting_styles", "table": "fighting_styles"},
    {"item_key": "categories", "table": "categories"},
)

# item key in Redis --> DB association table (relationship between tables)
MAPPINGS_ASSOCIATION_TABLES = (
    {
        "item_key": "voice_actors",
        "table": "characters_voice_actors",
        "left": "character",
        "col_left": "character_id",
        "col_right": "voice_actor_id",
    },
    {
        "item_key": "fighting_styles",
        "table": "characters_fighting_styles",
        "left": "character",
        "col_left": "character_id",
        "col_right": "fighting_style_id",
    },
    {
        "item_key": "categories",
        "table": "characters_categories",
        "left": "character",
        "col_left": "character_id",
        "col_right": "category_id",
    },
    {
        "item_key": "family_members",
        "table": "family_members",
        "left": "character",
        "col_left": "relative_left_id",
        "col_right": "relative_right_id",
    },
    {
        "item_key": "allegiances",
        "table": "allegiances",
        "left": "character",
        "col_left": "ally_left_id",
        "col_right": "ally_right_id",
    },
)

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
                # The scraped item stored in Redis does not contain any IDs.
                # Generate IDs for these fields before sending to DB.
                keys = (
                    "character",
                    "voice_actors",
                    "fighting_styles",
                    "categories",
                    "family_members",
                    "allegiances",
                )
                item_with_ids = assign_ids(item_sanitized, keys)

                for d in MAPPINGS_MODEL_TABLES:
                    x = item_with_ids["scraped_data"][d["item_key"]]
                    if isinstance(x, dict):
                        datum = x
                        data.append({"table": d["table"], "datum": datum})
                    else:
                        for datum in x:
                            data.append({"table": d["table"], "datum": datum})

                for a in MAPPINGS_ASSOCIATION_TABLES:
                    left = item_with_ids["scraped_data"][a["left"]]
                    for right in item_with_ids["scraped_data"][a["item_key"]]:
                        datum = {a["col_left"]: left["id"], a["col_right"]: right["id"]}
                        data.append({"table": a["table"], "datum": datum})
            else:
                n_invalid = n_invalid + 1
                logger.warning(f"{item['url']} contains invalid scraped data.")

    logger.debug(f"{len(redis_items)} items from Redis --> {len(data)} data.")
    return data


def store_in_db(engine, conn, table_names, data):
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

    model_tables = [d["table"] for d in MAPPINGS_MODEL_TABLES]
    association_tables = [d["table"] for d in MAPPINGS_ASSOCIATION_TABLES]
    if args.delete:
        # clean association tables first to respect DB contraints
        for table_name in association_tables:
            delete_all(engine, table_name)
        for table_name in model_tables:
            delete_all(engine, table_name)

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
        store_in_db(engine, conn, model_tables, data)
        store_in_db(engine, conn, association_tables, data)
        i0 = i0 + args.batch


if __name__ == "__main__":
    main()
