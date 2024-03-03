import unittest
from unittest.mock import patch

from mass.radio.authors_list.bot import make_authors_infos


class TestBot(unittest.TestCase):
    @patch('mass.radio.authors_list.bot.get_missing_authors')
    def test_make_authors_infos(self, mock_get_missing_authors):
        # Mock the return value of get_missing_authors
        mock_get_missing_authors.return_value = {
            'author1': 'John Doe',
            'author2': 'Jane Smith',
            'author3': 'Alice Johnson'
        }
        
        # Test case 1: Test when authors_n is empty
        authors_n = {}
        result = make_authors_infos(authors_n)
        self.assertEqual(result, {})
        
        # Test case 2: Test when authors_n has one author
        authors_n = {'author1': 'John Doe'}
        result = make_authors_infos(authors_n)
        self.assertEqual(result, {'author1': 'John Doe'})
        
        # Test case 3: Test when authors_n has multiple authors
        authors_n = {
            'author1': 'John Doe',
            'author2': 'Jane Smith',
            'author3': 'Alice Johnson'
        }
        result = make_authors_infos(authors_n)
        expected_result = {
            'author1': 'John Doe',
            'author2': 'Jane Smith',
            'author3': 'Alice Johnson'
        }
        self.assertEqual(result, expected_result)
        
        # Test case 4: Test when authors_n contains empty values
        authors_n = {
            'author1': '',
            'author2': 'Jane Smith',
            'author3': ''
        }
        result = make_authors_infos(authors_n)
        expected_result = {
            'author1': '',
            'author2': 'Jane Smith',
            'author3': ''
        }
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
