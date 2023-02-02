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
        url2 = "https://refactoring.guru/"
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

    def test_get_html_paragraph(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="paragraph")
        positional_index.run()
        index = positional_index.get_index()
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(index)
        self.assertEqual(index['act'][0], {"doc_id": 0, "position": [1589], "count": 1})
        self.assertEqual(index['design'][0], {"doc_id": 1, "position": [2, 16, 114, 181, 182, 193, 207], "count": 7})

    def test_run_index(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="title")
        positional_index.run()
        index = positional_index.get_index()
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(index)
        self.assertEqual(index['rate'][0], {'doc_id': 0, 'position': [1060], 'count': 1})
        self.assertEqual(index['after'][0], {'doc_id': 0, 'position': [298, 402, 1440], 'count': 3}) 

    def test_export_metadata(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="title")
        positional_index.run()
        metadata = positional_index.export_metadata()
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['nb_documents'], 2)
        self.assertEqual(metadata['nb_visited_urls'], 2)
        self.assertEqual(metadata['nb_failed_urls'], 0)
        self.assertEqual(metadata['nb_total_urls'], 2)

    def test_stopwords(self):
        # GIVEN
        url1 = "https://fr.wikipedia.org/wiki/Jeux_olympiques"
        url2 = "https://fr.wikipedia.org/wiki/Lotus_pedunculatus"
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="paragraph", delete_stopwords=True)
        positional_index.run()
        index = positional_index.get_index()
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(index)
        self.assertIn('la', index.keys())
        self.assertIn('le', index.keys())
        self.assertNotIn('les', index.keys())

    def test_stemmer(self):
        # GIVEN
        url1 = "https://fr.wikipedia.org/wiki/Jeux_olympiques"
        url2 = "https://fr.wikipedia.org/wiki/Lotus_pedunculatus"
        # WHEN
        positional_index = PositionalIndex(urls=[url1, url2], type="paragraph", use_stemmer=True)
        positional_index.run()
        index = positional_index.get_index()
        # THEN
        self.assertIsInstance(positional_index, PositionalIndex)
        self.assertIsNotNone(index)
        self.assertNotIn('olympique', index.keys())
        self.assertNotIn('inflammatoire', index.keys())
        self.assertIn('olymp', index.keys())
        self.assertIn('inflammatoir', index.keys())