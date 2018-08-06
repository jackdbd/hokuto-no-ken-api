# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import sqlalchemy as sa
from sqlalchemy.exc import NoSuchTableError

# from scrapy.exceptions import DropItem
from scrapy import log
from db_utils import get_table, create_characters_table, insert

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


class HokutoSQLitePipeline(object):

    def __init__(self):
        DB_NAME = "data.db"
        DB_PATH = os.path.join(ROOT, DB_NAME)
        DB_URI = f"sqlite:///{ROOT}/{DB_NAME}"
        if os.path.exists(DB_PATH):
            os.unlink(DB_PATH)
        self.engine = sa.create_engine(DB_URI)
        self.conn = self.engine.connect()
        try:
            self.table = get_table(self.engine, "characters")
        except NoSuchTableError:
            self.table = create_characters_table(DB_URI)

    def process_item(self, item, spider):
        datum = dict(item)
        insert(self.conn, self.table, datum)
        message = f'Character {datum["name"]} added to the database'
        log.msg(message, level=log.DEBUG, spider=spider)
        return item


class HokutoJSONLinesWriterPipeline(object):

    def __init__(self):
        self.file_path = os.path.join(ROOT, "characters.jsonl")
        self.fh = None
        if os.path.exists(self.file_path):
            os.unlink(self.file_path)

    def open_spider(self, spider):
        self.fh = open(self.file_path, "w")

    def close_spider(self, spider):
        self.fh.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.fh.write(line)
        return item
