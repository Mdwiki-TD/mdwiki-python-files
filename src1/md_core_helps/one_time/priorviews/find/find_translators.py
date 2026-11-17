"""

python3 c9/pwb.py priorviews/find/find_translators new

"""

import json
import logging
import os
import sys
from pathlib import Path

from md_core_helps.one_time.priorviews.bots import get_translator, helps
from md_core_helps.one_time.priorviews.lists.links_by_section import links_by_lang

logger = logging.getLogger(__name__)

Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)

file = f"{Dir2}/lists/translators_mdwiki_langs.json"

if not os.path.exists(file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump({}, f)

N_g = 0


def logem(file, data) -> None:
    logger.info(f"{len(data)} words")
    # dump tra_by_lang
    helps.dump_data(file, data)


def valid(x, tab, empty: str = "") -> bool:
    i = tab.get(x) or tab.get(x.lower())
    if not i or i == empty:
        return True
    return False


def get_t(links, lang, data):

    global N_g

    if lang not in data:
        data[lang] = {}

    m = 0


    if "onlynew" in sys.argv:
        links = [x for x in links if valid(x, data[lang])]

    lena = len(links)

    for title in links:

        title_lower = title.lower()

        m += 1

        value_in = data[lang].get(title_lower) or data[lang].get(title) or ""

        if "new" in sys.argv and value_in != "":
            continue

        logger.info(f"title: {m}/{lena} {title}, value_in:{value_in}")

        _value = get_translator.get_au(title, lang)

        if _value is None:
            _value = 0

        if value_in != 0 and _value == 0:
            continue

        if helps.is_ip(_value):
            continue

        data[lang][title_lower] = _value

        N_g += 1

        if N_g % 100 == 0:
            logem(file, data)

    return data


def start() -> None:

    langkeys = links_by_lang.keys()

    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]

    n = 0

    tra_by_lang = json.load(open(file, "r", encoding="utf-8"))

    for lang in langkeys:

        links = links_by_lang[lang]

        logger.info(f"lang: {lang}")
        logger.info(f"links: {len(links)}")

        n += 1

        tra_by_lang = get_t(links, lang, tra_by_lang)


    logem(file, tra_by_lang)

if __name__ == "__main__":
    start()
