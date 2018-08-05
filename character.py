# -*- coding: utf-8 -*-
import requests
import lxml.html


BASE_URL = "http://hokuto.wikia.com"
CHARACTER_URL = f"{BASE_URL}/wiki/Toki"


def scrape_field(node, index):
    # TODO: improve field parsing (e.g. Kenshiro's Fighting Style has two
    # entries. The url should be scraped too)
    if index is not None:
        selector = f"tr:nth-of-type({index}) > td"
        el = node.cssselect(selector)[0]
        field = el.text_content().strip("\n")
        return field
    else:
        return "NA"


def scrape(html):
    root = lxml.html.fromstring(html)
    infobox = root.cssselect("table.infobox")[0]

    # The first 2 <tr> contain no <th>
    i_offset = 2

    # it seems that the name is always at the same position in the infobox
    i_name_kanji = 1 + i_offset
    i_name_romaji = 2 + i_offset

    # A character might have none, some, or a combination of these fields
    i_fighting_style = None
    i_family = None
    i_allegiances = None
    i_appearances = None
    i_voice_actors = None

    elements = infobox.cssselect("tr > th")
    for i, el in enumerate(elements):
        # print(f"{i}: {el.text}")
        if "Fighting Style" in el.text:
            i_fighting_style = i + i_offset
        if "Family" in el.text:
            i_family = i + i_offset
        if "Allegiance" in el.text:
            i_allegiances = i + i_offset
        if "Appearances" in el.text:
            i_appearances = i + i_offset
        if "Voice actor" in el.text:
            i_voice_actors = i + i_offset

    for (key, index) in (
        ("Name (kanji)", i_name_kanji),
        ("Name (romaji)", i_name_romaji),
        ("Fighting Style", i_fighting_style),
        ("Family", i_family),
        ("Allegiance(s)", i_allegiances),
        ("Appearance(s)", i_appearances),
        ("Voice actor(s)", i_voice_actors),
    ):
        field = scrape_field(infobox, index)
        print(f"{key}: {field}")


if __name__ == "__main__":
    req = requests.get(CHARACTER_URL)
    scrape(req.text)
