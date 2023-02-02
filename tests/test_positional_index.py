from unittest import TestCase
from index.positional_index import PositionalIndex


class TestPositionalIndex(TestCase):
    def test_get_html_title(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        # title : Best Morning Routine: 21 Steps for a More Productive Day • Asana Asana Home Twitter Linkedin Instagram Facebook Youtube
        url2 = "https://refactoring.guru/"
        # title : Refactoring and Design Patterns
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2])
        result1 = positional_index.get_text_from_url(url=url1)
        result2 = positional_index.get_text_from_url(url=url2)
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(result1)
        self.assertIn('Best Morning Routine', result1)
        self.assertIsNotNone(result2)
        self.assertIn('Design Patterns', result2)

    def test_get_html_header(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        # title : Best Morning Routine: 21 Steps for a More Productive Day • Asana Asana Home Twitter Linkedin Instagram Facebook Youtube
        url2 = "https://refactoring.guru/"
        # title : Refactoring and Design Patterns
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="header")
        result1 = positional_index.get_text_from_url(url=url1)
        result2 = positional_index.get_text_from_url(url=url2)
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(result1)
        self.assertIn('21 steps for a more productive day', result1)
        self.assertIsNotNone(result2)
        self.assertIn('Design Patterns', result2)
