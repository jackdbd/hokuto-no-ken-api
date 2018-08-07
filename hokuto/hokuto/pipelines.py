# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import sqlalchemy as sa
from sqlalchemy.exc import NoSuchTableError

from scrapy.exceptions import DropItem
from scrapy import log
from db_utils import DB_PATH, DB_URI, get_table, create_characters_table, create_voice_actors_table, create_fighting_styles_table, insert

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


class HokutoSQLitePipeline(object):

    def __init__(self):
        # if os.path.exists(DB_PATH):
        #     os.unlink(DB_PATH)
        self.engine = sa.create_engine(DB_URI)
        self.conn = self.engine.connect()

        try:
            self.characters_table = get_table(self.engine, "characters")
        except NoSuchTableError:
            self.characters_table = create_characters_table(self.engine)

        try:
            self.voice_actors_table = get_table(self.engine, "voice_actors")
        except NoSuchTableError:
            self.voice_actors_table = create_voice_actors_table(self.engine)

        try:
            self.fighting_styles_table = get_table(self.engine, "fighting_styles")
        except NoSuchTableError:
            self.fighting_styles_table = create_fighting_styles_table(self.engine)

    def process_item(self, item, spider):
        if spider.name == "character":
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
