#!/usr/bin/python3
""" """

from __future__ import annotations
from pathlib import Path
import re

import wikitextparser as wtp


def test_plain_text_full():
    source_path = Path(__file__).parent / "wikitext.txt"
    output_path = Path(__file__).parent / "wikitext_output.txt"
    text = source_path.read_text(encoding="utf-8")

    parsed = wtp.parse(text)
    plain = parsed.plain_text()

    output_path.write_text(plain, encoding="utf-8")

    length = len(re.findall(r"\w+", plain))

    assert length == 249


def test_plain_text_full_with_template():
    source_path = Path(__file__).parent / "wikitext.txt"
    output_path = Path(__file__).parent / "templates_output.txt"
    text = source_path.read_text(encoding="utf-8")

    parsed = wtp.parse(text)
    for t in parsed.get_tags():
        t.string = ""

    parsed = wtp.parse(parsed.string)

    def clean(text: str) -> str:
        return wtp.parse(text).plain_text()

    def _replace_templates(template: wtp.Template):
        cleaned_arguments = [clean(x.value.strip()) for x in template.arguments if x.value and x.value.strip()]
        return "\n* ".join(x.strip() for x in cleaned_arguments if x.strip())

    plain = parsed.plain_text(replace_templates=_replace_templates)

    output_path.write_text(plain, encoding="utf-8")

    length = len(re.findall(r"\w+", plain))

    assert length == 363
