
import json
import re
import mwclient
import sys
from pathlib import Path

sys.argv.append("workibrahem")
from mdwiki_api.wiki_page import MainPage  # noqa: E402

RE_SVG_LANG = re.compile(r"\{\{\s*SVGLanguages\s*\|\s*([^}|]+)", re.I)
RE_TRANSLATE = re.compile(r"\*'''Translate''':\s*https://svgtranslate\.toolforge\.org/File:([^ \n]+)", re.I)

svg_languages = {}


def work_page(title):

    page = MainPage(title, "commons", family="wikimedia")

    if not page.exists():
        return False

    ns = page.namespace()

    if ns != 10:
        return False

    text = page.get_text()

    # 1. Existing SVGLanguages
    match = RE_SVG_LANG.search(text)
    if match:
        filename = match.group(1).strip()
        svg_languages[title] = filename
        return

    # 2. Missing, extract from Translate line
    trans_match = RE_TRANSLATE.search(text)
    if trans_match:
        filename = trans_match.group(1).strip()
        insert_text = f"*{{{{SVGLanguages|{filename}}}}}"
        new_text = re.sub(RE_TRANSLATE, lambda m: m.group(0) + "\n" + insert_text, text, count=1)
        svg_languages[title] = filename

        page.save(newtext=new_text, summary="Add [[Template:SVGLanguages]]", nocreate=1, minor="")


def start():

    site = mwclient.Site("commons.wikimedia.org")
    CATEGORY_NAME = "Pages using gadget owidslider"

    category = site.categories[CATEGORY_NAME]
    for page in category:
        work_page(page.name)

    # Save all data to JSON file
    with open(Path(__file__).parent / "svg_languages.json", "w", encoding="utf-8") as f:
        json.dump(svg_languages, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(svg_languages)} entries to svg_languages.json")


if __name__ == "__main__":
    start()
