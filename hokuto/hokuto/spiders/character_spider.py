import scrapy
from ..items import CharacterItem

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


def extract_appearances(selector):
    string = "".join(selector.extract()).strip("\n")
    i_manga_start = string.lower().find("manga")
    i_anime_start = string.lower().find("anime")

    if i_manga_start > -1:
        i_manga_stop = i_anime_start if i_anime_start else len(string)
        i_start = string[i_manga_start:i_manga_stop].find("(") + 1
        i_stop = string[i_manga_start:i_manga_stop].find(")")
        splits = string[i_start:i_stop].split()

        chapters = []
        chapter_singles = [int(s) for s in splits if s.isdigit()]
        chapters.extend(chapter_singles)

        chapter_ranges = [s for s in splits if "-" in s]
        for ch_range in chapter_ranges:
            ch_start, ch_stop = ch_range.strip(" ").strip(",").split("-")
            ch_range_start = int(ch_start)
            try:
                ch_range_stop = int(ch_stop)
            except ValueError:
                ch_range_stop = LAST_MANGA_CHAPTER
            chapters_in_range = list(range(ch_range_start, ch_range_stop + 1))
            chapters.extend(chapters_in_range)

        chapters.sort()
        first_appearance_manga = chapters[0]
        is_not_in_manga = False
    else:
        chapters = []
        first_appearance_manga = None
        is_not_in_manga = True

    if i_anime_start > -1:
        i_anime_stop = len(string)
        i_start = string[i_anime_start:i_anime_stop].find("(") + 1
        i_stop = string[i_anime_start:i_anime_stop].find(")")
        splits = string[i_start:i_stop].split()

        episodes = []
        episode_singles = [int(s) for s in splits if s.isdigit()]
        episodes.extend(episode_singles)
        episode_ranges = [s for s in splits if "-" in s]
        for ep_range in episode_ranges:
            ep_start, ep_stop = ep_range.strip(" ").strip(",").split("-")
            ep_range_start = int(ep_start)
            try:
                ep_range_stop = int(ep_stop)
            except ValueError:
                ep_range_stop = LAST_ANIME_EPISODE
            episodes_in_range = list(range(ep_range_start, ep_range_stop + 1))
            episodes.extend(episodes_in_range)

        episodes.sort()
        first_appearance_anime = episodes[0]
    else:
        episodes = []
        first_appearance_anime = None

    d = {
        "manga_chapters": chapters,
        "anime_episodes": episodes,
        "first_manga_chapter": first_appearance_manga,
        "first_anime_episode": first_appearance_anime,
        "is_not_in_manga": is_not_in_manga,
    }
    return d


class CharacterSpider(scrapy.Spider):
    name = "character"
    allowed_domains = ["http://hokuto.wikia.com"]
    start_urls = [
        "http://hokuto.wikia.com/wiki/Kenshiro",
        # "http://hokuto.wikia.com/wiki/Lin",
        # "http://hokuto.wikia.com/wiki/Shin",
        # "http://hokuto.wikia.com/wiki/Toki",
        # Joker was not in the original manga
        # "http://hokuto.wikia.com/wiki/Joker",
        # Asuka has a completely different page structure
        # "http://hokuto.wikia.com/wiki/Asuka",
        # # These two fail because they have a slightly different infobox
        # "http://hokuto.wikia.com/wiki/Page",
        # "http://hokuto.wikia.com/wiki/Pige",
    ]

    def parse(self, response):
        root = scrapy.Selector(response)
        tr_selectors = root.xpath('//table[@class="infobox"]/tr')
        name_kanji = tr_selectors[2].xpath("td/text()").extract()[0].strip("\n")
        name_romaji = tr_selectors[3].xpath("td/i/text()").extract()[0]

        d = {
            "name_kanji": name_kanji,
            "name_romaji": name_romaji,
            "avatar": None,
            "url": response.url,
            "fighting_styles": [],
            "family_members": [],
            "allegiances": [],
            "appearances": [],
            "voice_actors": [],
        }

        # A character might have none, some, or a combination of these fields
        for i, tr in enumerate(tr_selectors):
            th_text = tr.xpath("th/text()")
            # don't use map without list. Different pipelines might need the
            # same data
            if th_text:
                if "Fighting Style" in th_text.extract()[0]:
                    d["fighting_styles"] = list(
                        map(extract_fighting_style, tr.xpath("td/a"))
                    )
                if "Family" in th_text.extract()[0]:
                    d["family_members"] = list(
                        map(extract_family_member, tr.xpath("td/a"))
                    )
                if "Allegiance" in th_text.extract()[0]:
                    d["allegiances"] = list(map(extract_allegiance, tr.xpath("td/a")))
                if "Appearances" in th_text.extract()[0]:
                    d["appearances"] = extract_appearances(tr.xpath("td//text()"))
                if "Voice actor" in th_text.extract()[0]:
                    d["voice_actors"] = list(map(extract_voice_actor, tr.xpath("td/a")))
            else:
                d["avatar"] = tr.xpath("td/a/@href").extract()[0]

        item = CharacterItem(**d)
        yield item
