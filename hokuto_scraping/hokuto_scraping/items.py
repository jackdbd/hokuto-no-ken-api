# -*- coding: utf-8 -*-
"""Scrapy models for the items scraped by the spiders.

See Also:
    https://doc.scrapy.org/en/latest/topics/items.html
"""
import scrapy


class CharacterItem(scrapy.Item):
    name_kanji = scrapy.Field()
    name_romaji = scrapy.Field()
    avatar = scrapy.Field()
    url = scrapy.Field()
    fighting_styles = scrapy.Field()
    family_members = scrapy.Field()
    allegiances = scrapy.Field()
    appearances = scrapy.Field()
    voice_actors = scrapy.Field()
    # not sure if this is the best way to do it, but with this field we know if
    # we need to discard an item when we catch an exception in a spider.
    is_valid = scrapy.Field()
