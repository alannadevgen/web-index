from unittest import TestCase
from index.utils import Utils


class TestUtils(TestCase):
    def test_read_file(self):
        # GIVEN
        file_path = "data/crawled_urls.json"
        
        # WHEN
        util = Utils()
        file = util.read_json_file(path=file_path)
        
        # THEN
        self.assertIsInstance(util, Utils)
