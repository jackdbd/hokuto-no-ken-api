import os
from scrapy.http import HtmlResponse
from betamax.fixtures.unittest import BetamaxTestCase
from hokuto_scraping.spiders.characters import Characters


class TestCharacters(BetamaxTestCase):

    def test_parse_page_kenshiro(self):
        url = 'http://hokuto.wikia.com/wiki/Kenshiro'
        # http response is recorded in a betamax cassette
        response = self.session.get(url)
        # forge a scrapy response to test
        scrapy_response = HtmlResponse(body=response.content, url=url)

        spider = Characters()
        result = spider.parse_page(scrapy_response)
        d = next(result)
        data = d['scraped_data']

        self.assertEqual(data['name'], 'Kenshiro')
        self.assertEqual(len(data['allegiances']), 0)
        self.assertEqual(data['first_appearance'], {'manga': 1, 'anime': 1})
        
        with self.assertRaises(StopIteration):
            next(result)
