from unittest import TestCase
from index.non_positional_index import NonPositionalIndex


class TestPositionalIndex(TestCase):
    def test_get_html_title(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        # title : Best Morning Routine: 21 Steps for a More Productive Day • Asana Asana Home Twitter Linkedin Instagram Facebook Youtube
        url2 = "https://refactoring.guru/"
        # title : Refactoring and Design Patterns
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2])
        result1 = non_positional_index.get_text_from_url(url=url1)
        result2 = non_positional_index.get_text_from_url(url=url2)
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(result1)
        self.assertIn('Best Morning Routine', result1)
        self.assertIsNotNone(result2)
        self.assertIn('Design Patterns', result2)


    def test_get_html_fail(self):
        # GIVEN
        url1 = "https://www.degriffelectromenager.com/"
        url2 = "http://www.amisducadrenoir.fr/"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2])
        result1 = non_positional_index.get_text_from_url(url=url1)
        result2 = non_positional_index.get_text_from_url(url=url2)
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNone(result1)
        self.assertIsNone(result2)
        self.assertRaises(Exception, result1)
        self.assertRaises(Exception, result2)

    def test_get_html_header(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="header")
        result1 = non_positional_index.get_text_from_url(url=url1)
        result2 = non_positional_index.get_text_from_url(url=url2)
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(result1)
        self.assertIn('21 steps for a more productive day', result1)
        self.assertIsNotNone(result2)
        self.assertIn('Design Patterns', result2)

    def test_get_html_paragraph(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="paragraph")
        non_positional_index.run()
        index = non_positional_index.get_index()
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(index)
        self.assertEqual(index['schedule'][0], {"doc_id": 0, "count": 1})
        self.assertEqual(index['enter'][0], {"doc_id": 1, "count": 1})

    def test_run_index(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="title")
        non_positional_index.run()
        index = non_positional_index.get_index()
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(index)
        self.assertEqual(index['rate'][0], {'doc_id': 0, 'count': 1})
        self.assertEqual(index['affirmations'][0], {'doc_id': 0, 'count': 7}) 
    

    def test_export_metadata(self):
        # GIVEN
        url1 = "https://asana.com/resources/best-morning-routine"
        url2 = "https://refactoring.guru/"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="title")
        non_positional_index.run()
        metadata = non_positional_index.export_metadata()
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
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
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="paragraph", delete_stopwords=False)
        non_positional_index.run()
        index = non_positional_index.get_index()
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(index)
        self.assertIn('ce', index.keys())
        self.assertIn('le', index.keys())
        self.assertIn('ceux', index.keys())

    
    def test_stemmer(self):
        # GIVEN
        url1 = "https://fr.wikipedia.org/wiki/Jeux_olympiques"
        url2 = "https://fr.wikipedia.org/wiki/Lotus_pedunculatus"
        # WHEN
        non_positional_index = NonPositionalIndex(urls=[url1, url2], type="paragraph", use_stemmer=True)
        non_positional_index.run()
        index = non_positional_index.get_index()
        # THEN
        self.assertIsInstance(non_positional_index, NonPositionalIndex)
        self.assertIsNotNone(index)
        self.assertNotIn('olympique', index.keys())
        self.assertNotIn('inflammatoire', index.keys())
        self.assertIn('olymp', index.keys())
        self.assertIn('inflammatoir', index.keys())
