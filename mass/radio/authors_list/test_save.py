import unittest
from unittest.mock import patch

from mass.radio.authors_list.save import sa


class TestSave(unittest.TestCase):
    @patch('mass.radio.authors_list.save.ncc_MainPage')
    def test_sa(self, mock_ncc_MainPage):
        # Mock the return value of ncc_MainPage.exists()
        mock_ncc_MainPage.return_value.exists.return_value = True
        
        # Test case 1: Test when au_infos is empty
        au_infos = {}
        sa(au_infos)
        
        # Assert that ncc_MainPage.save() is called with the correct arguments
        mock_ncc_MainPage.return_value.save.assert_called_with(newtext='* All Authors: 0\n\n{| class="wikitable sortable"\n|-\n! # !! Author !! Cases !! Url !! Location\n|}\n\n', summary='update')
        
        # Test case 2: Test when au_infos is not empty
        au_infos = {
            'author1': {
                'cases': 10,
                'url': 'https://example.com/author1',
                'location': 'Location 1'
            },
            'author2': {
                'cases': 5,
                'url': 'https://example.com/author2',
                'location': 'Location 2'
            }
        }
        sa(au_infos)
        
        # Assert that ncc_MainPage.save() is called with the correct arguments
        mock_ncc_MainPage.return_value.save.assert_called_with(newtext='* All Authors: 2\n\n{| class="wikitable sortable"\n|-\n! # !! Author !! Cases !! Url !! Location\n|-\n! 1\n| author1\n| 10\n| https://example.com/author1\n| Location 1\n|-\n! 2\n| author2\n| 5\n| https://example.com/author2\n| Location 2\n|}\n\n', summary='update')

if __name__ == '__main__':
    unittest.main()
