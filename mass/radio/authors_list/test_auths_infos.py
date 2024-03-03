import unittest
from unittest.mock import patch

from mass.radio.authors_list.auths_infos import (get_author_infos,
                                                 get_user_infos)


class TestAuthsInfos(unittest.TestCase):
    @patch('mass.radio.authors_list.auths_infos.get_user_infos')
    def test_get_author_infos(self, mock_get_user_infos):
        # Mock the return value of get_user_infos
        mock_get_user_infos.return_value = {
            "url": "https://example.com",
            "location": "Test Location"
        }

        # Test case 1: Valid input
        auth = "Test Author"
        first_case_url = "https://example.com/case1"
        expected_result = {
            "url": "https://example.com",
            "location": "Test Location"
        }
        result = get_author_infos(auth, first_case_url)
        self.assertEqual(result, expected_result)

        # Test case 2: Empty input
        auth = ""
        first_case_url = ""
        expected_result = {
            "url": "",
            "location": ""
        }
        result = get_author_infos(auth, first_case_url)
        self.assertEqual(result, expected_result)

        # Test case 3: Missing location
        auth = "Test Author"
        first_case_url = "https://example.com/case2"
        expected_result = {
            "url": "https://example.com",
            "location": ""
        }
        result = get_author_infos(auth, first_case_url)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
