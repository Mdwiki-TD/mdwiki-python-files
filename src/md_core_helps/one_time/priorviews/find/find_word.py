"""

python3 core8/pwb.py priorviews/find/find_word -lang:ar
python3 core8/pwb.py priorviews/find/find_word new

"""

import json

# ---
import logging
import os
import sys
from pathlib import Path

from md_core_helps.one_time.priorviews.bots import count_words, helps
from md_core_helps.one_time.priorviews.lists.links_by_section import links_by_lang

logger = logging.getLogger(__name__)

TEST = False

Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)


def log_words(file_path, data) -> None:
    logger.info(f"<<yellow>> {len(data)} words")
    helps.dump_data(file_path, data)


def valid(x, tab, empty: str = "") -> bool:
    i = tab.get(x) or tab.get(x.lower())
    if not i or i == empty:
        return True
    return False


def get_w(links, lang, _words_by_lang):
    # ---
    if lang not in _words_by_lang:
        _words_by_lang[lang] = {}
    # ---
    m = 0
    # ---
    if "onlynew" in sys.argv:
        # links = [ x for x in links if not x in _words_by_lang[lang] or _words_by_lang[lang][x] == 0]
        links = [x for x in links if valid(x, _words_by_lang[lang], empty=0)]
    # ---
    lena = len(links)
    # ---
    for title in links:
        # ---
        title_lower = title.lower()
        # ---
        m += 1
        # ---
        words_in = _words_by_lang[lang].get(title_lower, 0)
        # ---
        if "new" in sys.argv and words_in > 40:
            continue
        # ---
        logger.info(f"<<yellow>> title: {m}/{lena} {title}, words_in:{words_in}")
        # ---
        _words = count_words.get_words(title, lang)
        # ---
        if _words is None:
            _words = 0
        # ---
        if words_in != 0 and _words == 0:
            continue
        # ---
        _words_by_lang[lang][title_lower] = _words
        # ---
    # ---
    return _words_by_lang


def start() -> None:
    # ---
    langkeys = links_by_lang.keys()
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]
    # ---
    n = 0
    # ---
    file = f"{Dir2}/lists/words_mdwiki_langs.json"
    # ---
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f)
    # ---
    words_by_lang = json.load(open(file, "r", encoding="utf-8"))
    # ---
    for lang in langkeys:
        # ---
        links = links_by_lang[lang]
        # ---
        logger.info(f"lang: {lang}")
        logger.info(f"links: {len(links)}")
        # ---
        n += 1
        # ---
        words_by_lang = get_w(links, lang, words_by_lang)
        # ---
        log_words(file, words_by_lang)
        # ---
    # ---
    log_words(file, words_by_lang)


if __name__ == "__main__":
    start()
