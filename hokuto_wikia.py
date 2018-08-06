# -*- coding: utf-8 -*-
import scrapy


class HokutoWikiaSpider(scrapy.Spider):
    name = "hokuto_wikia"
    allowed_domains = ["hokuto.wikia.com"]
    start_urls = ["http://hokuto.wikia.com/"]

    def parse(self, response):
        pass
