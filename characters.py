# -*- coding: utf-8 -*-
import requests
import lxml.html


BASE_URL = "http://hokuto.wikia.com"
CHARACTERS_URL = f"{BASE_URL}/wiki/List_of_Hokuto_no_Ken_characters"


def create_character(el, is_not_in_manga):
    if "(page does not exist)" in el.attrib["title"]:
        url = None
    else:
        url = f'{BASE_URL}{el.attrib["href"]}'
    character = {"name_romaji": el.text, "url": url, "is_not_in_manga": is_not_in_manga}
    # print(f"{character}")
    return character


def scrape_characters(root, selector, is_not_in_manga):
    elements = root.cssselect(selector)
    characters = [create_character(el, is_not_in_manga) for el in elements]
    return characters


def scrape(html):
    root = lxml.html.fromstring(html)
    characters_in_manga = scrape_characters(
        root, "div#mw-content-text > ul > li > a", False
    )
    print(f"{len(characters_in_manga)} characters in the original manga")
    print("Characters in the original manga", characters_in_manga)


if __name__ == "__main__":
    req = requests.get(CHARACTERS_URL)
    scrape(req.text)
