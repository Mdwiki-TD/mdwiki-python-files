import unittest
from unittest.mock import patch

from mass.radio.st3.count import start
from md_core.mdcount.copy_word_table import All


class TestCount(unittest.TestCase):
    @patch('mass.radio.st3.count.get_studies')
    def test_start_function(self, mock_get_studies):
        # Create test data for ids_tab
        ids_tab = {
            "id1": {
                "caseId": "case1",
                "studies": ["study1", "study2"]
            },
            "id2": {
                "caseId": "case2",
                "studies": ["study3"]
            }
        }

        # Mock the get_studies function
        mock_get_studies.return_value = 5

        # Call the start function
        start(ids_tab)

        # Assert the expected results
        self.assertEqual(2, mock_get_studies.call_count)
        self.assertEqual(10, All.studies)
        self.assertEqual(10, All.images)

        # Reset the All class attributes
        All.studies = 0
        All.images = 0

if __name__ == '__main__':
    unittest.main()
