import unittest
from datetime import date, timedelta
import xml.etree.ElementTree as ET
from refresh import parse_feed, articles_markup, parse_calendar, make_snake

class RefreshTests(unittest.TestCase):
    def test_rss_filters_bad_links_and_limits(self):
        rss='<rss><channel><item><title>bad</title><link>javascript:alert(1)</link></item>'+''.join(f'<item><title>Article {n}</title><link>https://example.com/{n}</link></item>' for n in range(5))+'</channel></rss>'
        result=parse_feed(rss)
        self.assertEqual(len(result),3)
        self.assertEqual(result[0],('Article 0','https://example.com/0'))
    def test_atom_prefers_article_link(self):
        atom='<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Note</title><link rel="self" href="https://example.com/feed"/><link href="https://example.com/note"/></entry></feed>'
        self.assertEqual(parse_feed(atom),[('Note','https://example.com/note')])
    def test_feed_text_cannot_inject_markup(self):
        result=articles_markup([('<img src=x onerror=alert(1)>','https://example.com/?a="b"')])
        self.assertNotIn('<img',result)
        self.assertIn('&quot;',result)
    def test_empty_feed_rejected(self):
        with self.assertRaises(ValueError): parse_feed('<rss><channel/></rss>')
    def test_incomplete_calendar_rejected(self):
        with self.assertRaises(ValueError): parse_calendar('<td data-date="2026-01-01" data-level="1">')
    def test_calendar_dates_preserved_in_valid_svg(self):
        start=date(2025,9,14)
        source=''.join(f'<td data-date="{start+timedelta(days=i)}" data-level="{i%5}">' for i in range(365))
        days=parse_calendar(source); svg=make_snake(days); ET.fromstring(svg)
        self.assertEqual(len(days),365)
        self.assertIn('2025-09-14: activity level 0',svg)
        self.assertIn('prefers-reduced-motion',svg)

if __name__=='__main__': unittest.main()
