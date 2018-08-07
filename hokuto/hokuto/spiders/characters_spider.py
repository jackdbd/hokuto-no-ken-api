from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
from .character_spider import CharacterSpider


class CharactersSpider(CrawlSpider):
    name = "characters"
    allowed_domains = ["hokuto.wikia.com"]
    start_urls = ["http://hokuto.wikia.com/wiki/List_of_Hokuto_no_Ken_characters"]

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

    def parse_item(self, response):
        cs = CharacterSpider()
        try:
            item = next(cs.parse(response))
        except IndexError:
            raise DropItem

        yield item


# root = scrapy.Selector(response)
#
# li = root.xpath('//div[@id="mw-content-text"]/ul/li')
# # Kenshiro: <b><a></a></b>
# # Characters not in manga: <i><a></a></i>
# # Everyone else: <a></a>
# for (is_not_in_manga, xpath_query) in (
#     (False, "b/a"), (True, "i/a"), (False, "a")
# ):
#     characters = li.xpath((xpath_query))
#     for character in characters:
#         name = character.xpath("text()").extract()[0]
#         if "(page does not exist)" in character.attrib["title"]:
#             url = None
#         else:
#             url = character.xpath("@href").extract()[0]
#
#         item = LegacyCharacterItem(
#             name=name, is_not_in_manga=is_not_in_manga, url=url
#         )
#         yield item
