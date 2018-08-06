# -*- coding: utf-8 -*-
"""Scrapy models for the items scraped by the spiders.

See Also:
    https://doc.scrapy.org/en/latest/topics/items.html
"""
import scrapy


class LegacyCharacterItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    is_not_in_manga = scrapy.Field()


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
