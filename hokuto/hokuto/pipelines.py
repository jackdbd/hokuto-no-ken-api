# -*- coding: utf-8 -*-
"""Item pipelines.

Don't forget to add your pipeline to the ITEM_PIPELINES setting (either in
settings.py on as custom_settings in one or more spiders.

See Also
    https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
import os
import sqlalchemy as sa
from scrapy.exceptions import DropItem
from scrapy import log
from dotenv import find_dotenv, load_dotenv
from .db_utils import get_table, insert


load_dotenv(find_dotenv(".env"))
HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DB_NAME = os.environ.get("LOCAL_DB")
DB_PATH = os.path.join(ROOT, DB_NAME)
DB_URI = f"sqlite:///{ROOT}/{DB_NAME}"


class SQLDbPipeline(object):

    def __init__(self):
        self.engine = sa.create_engine(DB_URI)
        self.conn = self.engine.connect()
        self.characters_table = get_table(self.engine, "characters")
        self.voice_actors_table = get_table(self.engine, "voice_actors")
        self.fighting_styles_table = get_table(self.engine, "fighting_styles")

    def process_item(self, item, spider):
        if not item["is_valid"]:
            raise DropItem

        datum = {
            "avatar": item["avatar"],
            "name_kanji": item["name_kanji"],
            "name_romaji": item["name_romaji"],
            "url": item["url"],
            "is_not_in_manga": item["appearances"]["is_not_in_manga"],
            "first_manga_chapter": item["appearances"]["first_manga_chapter"],
            "first_anime_episode": item["appearances"]["first_anime_episode"],
        }
        insert(self.conn, self.characters_table, datum)
        message = f'Character {datum["name_romaji"]} added to the database'
        log.msg(message, level=log.DEBUG, spider=spider)

        for datum in item["fighting_styles"]:
            insert(self.conn, self.fighting_styles_table, datum)
            message = f'Fighting style {datum["name"]} added to the database'
            log.msg(message, level=log.DEBUG, spider=spider)

        for datum in item["voice_actors"]:
            insert(self.conn, self.voice_actors_table, datum)
            message = f'Voice actor {datum["name"]} added to the database'
            log.msg(message, level=log.DEBUG, spider=spider)

        return item
