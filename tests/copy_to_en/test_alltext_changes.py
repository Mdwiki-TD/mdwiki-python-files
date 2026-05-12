"""
python3 core8/pwb.py copy_to_en/tests/test_alltext_changes

"""

from pathlib import Path

import pytest
from copy_to_en.bots import alltext_changes


class TestAllTextChanges:
    def setup_method(self):
        self.test_file = Path(__file__).parent / "sample_text.txt"
        with open(self.test_file, "r", encoding="utf-8") as f:
            self.test_text = f.read()

    def test_change_last_section(self):
        result = alltext_changes.do_alltext_changes(self.test_text)
        assert "[[Category:" not in result.split("\n")[-1]
        assert "[[azb:" not in result

    def test_do_all_text(self):
        result = alltext_changes.do_all_text(self.test_text, "12345", "{{#unlinkedwikibase:id=Q123}}")
        assert "{{mdwiki revid|12345}}" in result
        assert "[[Category:Mdwiki Translation Dashboard articles/fulltext]]" in result
