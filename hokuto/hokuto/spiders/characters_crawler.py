"""Spider to scrape all characters on Hokuto Renkitōza.
"""
import logging
import datetime
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..settings import BOT_NAME


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter_str = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# https://en.wikipedia.org/wiki/List_of_Fist_of_the_North_Star_chapters
LAST_MANGA_CHAPTER = 245
LAST_ANIME_EPISODE = 152


def extract_voice_actor(selector):
    name = selector.xpath("text()").extract()[0]
    title = selector.xpath("@title").extract()[0]
    if "page does not exist" in title:
        url = None
    else:
        url = selector.xpath("@href").extract()[0]
    d = {"name": name, "url": url}
    return d


def extract_fighting_style(selector):
    name = selector.xpath("text()").extract()[0]
    url = selector.xpath("@href").extract()[0]
    d = {"name": name, "url": url}
    return d


def extract_family_member(selector):
    name = selector.xpath("text()").extract()[0]
    url = selector.xpath("@href").extract()[0]
    d = {"name": name, "url": url}
    return d


def extract_allegiance(selector):
    name = selector.xpath("text()").extract()[0]
    url = selector.xpath("@href").extract()[0]
    d = {"name": name, "url": url}
    return d


def extract_first_appearance(string, type_, last_possible):
    """Extract the first appearance of the character in manga or anime

    Note: the complete list of manga_chapters and anime_episodes seems
    incorrect on Hokuto Renkitōza.

    Parameters
    ----------
    string : str
        entire appearances string from the infobox on Hokuto Renkitōza
    type_ : str
        "manga", "anime"
    last_possible : int
        last manga chapter or last anime episode

    Returns
    -------
    d : dict
    """
    i_start = string.lower().find(type_)
    if i_start > -1:
        substring = string[i_start:]
        i0 = substring.find("(") + 1
        i1 = substring[i0:].find(")")
        splits = substring[i0:i0 + i1].split()

        appearances = []
        appearances_single = [int(s) for s in splits if s.isdigit()]
        appearances.extend(appearances_single)

        appearances_range = [s for s in splits if "-" in s]
        for app_range in appearances_range:
            app_start, app_stop = app_range.strip(" ").strip(",").split("-")
            app_range_start = int(app_start)
            try:
                app_range_stop = int(app_stop)
            except ValueError:
                app_range_stop = last_possible
            appearances_in_range = list(range(app_range_start, app_range_stop + 1))
            appearances.extend(appearances_in_range)

        appearances.sort()
        first_appearance = appearances[0]
    else:
        first_appearance = None

    return first_appearance


def extract_appearances(selector):
    string = "".join(selector.extract()).strip("\n")
    d = {
        "manga": extract_first_appearance(string, "manga", LAST_MANGA_CHAPTER),
        "anime": extract_first_appearance(string, "anime", LAST_ANIME_EPISODE),
    }
    return d


def scrape_infobox(selector_list, url):
    """Extract data from the character's infobox on Hokuto Renkitōza.

    Note: the structure of the infox is not consistent throughout Hokuto
    Renkitōza. Some fields might be missing on any given character's page.

    Parameters
    ----------
    selector_list : scrapy.selector.unified.SelectorList
    url : str

    Returns
    -------
    d : dict
    """
    tr_selectors = selector_list.xpath("tr")
    # A character might have none, some, or a combination of these fields
    name_kanji = None
    name_romaji = None
    avatar = None
    first_appearance = None
    fighting_styles = []
    family_members = []
    allegiances = []
    voice_actors = []
    for i, tr in enumerate(tr_selectors):
        th_text = tr.xpath("th/text()")
        # don't use map without list. Different pipelines might need the
        # same data
        if th_text:
            if "Name in Kanji" in th_text.extract_first():
                name_kanji = tr.xpath("td/text()").extract_first().strip("\n")
            if "Name in Romaji" in th_text.extract_first():
                name_romaji = tr.xpath("td/i/text()").extract_first()
            if "Fighting Style" in th_text.extract_first():
                fighting_styles = list(map(extract_fighting_style, tr.xpath("td/a")))
            if "Family" in th_text.extract_first():
                family_members = list(map(extract_family_member, tr.xpath("td/a")))
            if "Allegiance" in th_text.extract_first():
                allegiances = list(map(extract_allegiance, tr.xpath("td/a")))
            if "Appearances" in th_text.extract_first():
                first_appearance = extract_appearances(tr.xpath("td//text()"))
            if "Voice actor" in th_text.extract_first():
                voice_actors = list(map(extract_voice_actor, tr.xpath("td/a")))
        else:
            avatar = tr.xpath("td/a/@href").extract_first()

    d = {
        "name_kanji": name_kanji,
        "name_romaji": name_romaji,
        "avatar": avatar,
        "fighting_styles": fighting_styles,
        "family_members": family_members,
        "allegiances": allegiances,
        "first_appearance": first_appearance,
        "voice_actors": voice_actors,
    }
    if any([x is None for x in d.values()]):
        logger.warning(f"Check {url}: could not scrape some fields.")
    return d


def scrape_page(selector_list, url):
    # TODO: extract "voiced by" (e.g. Asuka, Barona)
    name_romaji = selector_list.xpath("text()").extract_first()
    if name_romaji is None:
        logger.warning(f"Name (romaji) not scraped at {url}")

    name_kanji = selector_list.xpath("//span[@lang='ja']/text()").extract_first()
    if name_kanji is None:
        logger.warning(f"Name (kanji) not scraped at {url}")
    d = {"name_romaji": name_romaji, "name_kanji": name_kanji}
    return d


class CharactersCrawler(CrawlSpider):
    name = "characters_crawler"
    allowed_domains = ["hokuto.wikia.com"]
    start_urls = [
        "http://hokuto.wikia.com/wiki/List_of_Hokuto_no_Ken_characters",
        "http://hokuto.wikia.com/wiki/List_of_Jibo_no_Hoshi_characters",
        "http://hokuto.wikia.com/wiki/List_of_Shirogane_no_Seija_characters",
        "http://hokuto.wikia.com/wiki/List_of_S%C5%8Dkoku_no_Gar%C5%8D_characters",
        "http://hokuto.wikia.com/wiki/List_of_Ten_no_Haoh_characters",
        "http://hokuto.wikia.com/wiki/List_of_Souten_no_Ken_characters",
        "http://hokuto.wikia.com/wiki/List_of_Souten_no_Ken_Regenesis_characters",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=("^http:\/\/hokuto\.wikia\.com\/wiki\/.+$",),
                restrict_xpaths=("//div[@id='mw-content-text']/ul//li",),
            ),
            callback="parse_page",
            follow=False,
        ),
    )
    custom_settings = {
        "ITEM_PIPELINES": {
            f"{BOT_NAME}.pipelines.DropItemPipeline": 100,
            "scrapy_redis.pipelines.RedisPipeline": 300,
        }
    }

    def parse_page(self, response):
        url = response.url
        tz = datetime.datetime.utcnow().astimezone().tzinfo
        crawled_at = datetime.datetime.now(tz)

        has_page = False if "?action=edit" in response.url else True
        if not has_page:
            logger.warning(f"Cannot scrape. Page does not exist: {url}")
            scraped_data = None
        else:
            name = url.split("/")[-1]
            # This character appears in these categories on Hokuto Renkitōza
            selector_list = response.xpath(
                "//div[@class='page-header__categories-links']/a"
            )
            categories = [
                {
                    "name": c.xpath("text()").extract(),
                    "link": c.xpath("@href").extract(),
                }
                for c in selector_list
            ]

            scraped_at = datetime.datetime.now(tz)
            common_data = {
                "name": name, "scraped_at": str(scraped_at), "categories": categories
            }
            infobox = response.xpath('//table[@class="infobox"]')
            if not infobox:
                dt = response.xpath("//dl/dt")
                page_data = scrape_page(dt, url)
                scraped_data = {**common_data, **page_data}
            else:
                infobox_data = scrape_infobox(infobox, url)
                scraped_data = {**common_data, **infobox_data}

        d = {
            "url": response.url,
            "crawled_at": str(crawled_at),
            "tz": str(tz),
            "scraped_data": scraped_data,
        }
        yield d
