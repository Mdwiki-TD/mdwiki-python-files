"""
python3 core8/pwb.py copy_to_en/tests/test_alltext_changes

"""
import unittest
from pathlib import Path
from copy_to_en.bots import alltext_changes


class TestAllTextChanges(unittest.TestCase):
    def setUp(self):
        self.test_file = Path(__file__).parent / "sample_text.txt"
        with open(self.test_file) as f:
            self.test_text = f.read()

    def test_change_last_section(self):
        result = alltext_changes.do_alltext_changes(self.test_text)
        self.assertNotIn("[[Category:", result.split("\n")[-1])
        self.assertNotIn("[[azb:", result)

    def test_do_all_text(self):
        result = alltext_changes.do_all_text(self.test_text, "12345", "{{#unlinkedwikibase:id=Q123}}")
        self.assertIn("{{mdwiki revid|12345}}", result)
        self.assertIn("[[Category:Mdwiki Translation Dashboard articles/fulltext]]", result)
        # self.assertIn("[[Category:Mdwiki Translation Dashboard articles/fulltext]]!", result)


if __name__ == "__main__":
    unittest.main()
