import scrapy
from ..items import HokutoNoKenCharacter


class CharactersSpider(scrapy.Spider):
    name = "characters"
    allowed_domains = ["http://hokuto.wikia.com"]
    start_urls = ["http://hokuto.wikia.com/wiki/List_of_Hokuto_no_Ken_characters"]

    def parse(self, response):
        root = scrapy.Selector(response)

        li = root.xpath('//div[@id="mw-content-text"]/ul/li')
        # Kenshiro: <b><a></a></b>
        # Characters not in manga: <i><a></a></i>
        # Everyone else: <a></a>
        for (is_not_in_manga, xpath_query) in (
            (False, "b/a"), (True, "i/a"), (False, "a")
        ):
            characters = li.xpath((xpath_query))
            for character in characters:
                name = character.xpath("text()").extract()[0]
                if "(page does not exist)" in character.attrib["title"]:
                    url = None
                else:
                    url = character.xpath("@href").extract()[0]

                item = HokutoNoKenCharacter(
                    name=name, is_not_in_manga=is_not_in_manga, url=url
                )
                yield item
