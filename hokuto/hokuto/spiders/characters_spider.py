from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .character_spider import CharacterSpider
from ..items import CharacterItem


class CharactersSpider(CrawlSpider):
    name = "characters"
    allowed_domains = ["hokuto.wikia.com"]
    start_urls = [
        "http://hokuto.wikia.com/wiki/List_of_Hokuto_no_Ken_characters",
        # this should not be picked by the spider
        "http://hokuto.wikia.com/wiki/Hokuto_no_Ken_Online",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=("^http:\/\/hokuto\.wikia\.com\/wiki\/\w+(\.){0,1}$",),
                restrict_xpaths=("//div[@id='mw-content-text']/ul/li",),
            ),
            callback="parse_item",
            follow=True,
        ),
    )
    custom_settings = {"ITEM_PIPELINES": {"hokuto.pipelines.SQLDbPipeline": 300}}

    def parse_item(self, response):
        cs = CharacterSpider()
        try:
            item = next(cs.parse(response))
            item["is_valid"] = True
        except IndexError:
            # not sure if this is a good way to identify invalid items (to drop
            # in item pipelines)
            d = {x: False for x in CharacterItem.fields.keys()}
            item = CharacterItem(**d)

        yield item
