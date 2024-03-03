import unittest
from unittest.mock import patch

from mass.radio.authors_list.bot import make_authors_infos, make_authors_list


class TestBot(unittest.TestCase):
    @patch('mass.radio.authors_list.bot.get_missing_authors')
    def test_make_authors_list(self, mock_get_missing_authors):
        # Mock the return value of get_missing_authors
        mock_get_missing_authors.return_value = {
            "author1": ["case1", "case2"],
            "author2": ["case3"],
            "author3": []
        }

        # Test case 1: Valid input
        authors_n = {
            "author1": "Author 1",
            "author2": "Author 2",
            "author3": "Author 3"
        }
        expected_result = {
            "Author 1": ["author1"],
            "Author 2": ["author2"],
            "Author 3": ["author3"]
        }
        result = make_authors_list(authors_n)
        self.assertEqual(result, expected_result)

        # Test case 2: Empty input
        authors_n = {}
        expected_result = {}
        result = make_authors_list(authors_n)
        self.assertEqual(result, expected_result)

    def test_make_authors_infos(self):
        # Test case 1: Valid input
        auths = {
            "Author 1": ["case1", "case2"],
            "Author 2": ["case3"],
            "Author 3": []
        }
        expected_result = {
            "Author 1": {},
            "Author 2": {},
            "Author 3": {}
        }
        result = make_authors_infos(auths)
        self.assertEqual(result, expected_result)

        # Test case 2: Empty input
        auths = {}
        expected_result = {}
        result = make_authors_infos(auths)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
