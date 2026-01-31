"""

python3 core8/pwb.py WHOem/find_views_by_lang

"""

import json

# ---
import logging
import os
import sys
from pathlib import Path

from apis.mw_views import PageviewsClient

logger = logging.getLogger(__name__)

view_bot = PageviewsClient()

# ---
TEST = False
# ---
Dir = Path(__file__).parent
# ---
file = f"{Dir}/lists/views.json"
# ---
if not os.path.exists(file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump({}, f)
# ---
with open(file, "r", encoding="utf-8") as f:
    ViewsData = json.load(f)
# ---
N_g = {1: 0}


def dump_data(file, data):
    logger.info(f"<<green>> () file:{file}.")
    logger.info(f"<<yellow>> {len(data)} views")
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except KeyboardInterrupt:
        logger.error("<<red>> keyboard interrupt sys.exit()")
        # ---
        with open(f"{file}_1", "w", encoding="utf-8") as f:
            json.dump(data, f)
        # ---
        sys.exit()
    except Exception as e:
        logger.error(f"<<red>> dump Error: {e}")


def get_v(lang, links, lang_links_mdtitle_s):
    # ---
    global ViewsData
    # ---
    len_p = len(links)
    # -- -
    if "new" in sys.argv:
        links = {x: t for x, t in links.items() if ViewsData[t].get(lang, {}).get("views", 0) == 0}
        de = len_p - len(links)
        logger.info(f"de: {de}")
    # ---
    # split links to groups by 50 titles
    for i in range(0, len(links), 50):
        # ---
        group = dict(list(links.items())[i : i + 50])
        # ---
        new_data = view_bot.article_views_new(
            f"{lang}.wikipedia", group.keys(), granularity="monthly", start="20150701", end="20300101"
        )
        # ---
        # {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }
        # ---
        for title, tabe in new_data.items():
            # ---
            mdtitle = lang_links_mdtitle_s.get(lang, {}).get(title, None)
            # ---
            if mdtitle is None:
                continue
            # ---
            all_views = tabe["all"]
            # ---
            viws_in = ViewsData[mdtitle].get(lang, {}).get("views", 0)
            # ---
            logger.info(f"t: {title} - {lang} - views: {all_views}")
            # ---
            # ViewsData.setdefault(mdtitle, {})[lang] = ViewsData[mdtitle].setdefault(lang, {})
            # ---
            # ViewsData.setdefault(mdtitle, {})
            if mdtitle not in ViewsData.keys():
                ViewsData[mdtitle] = {}
            # ---
            # ViewsData[mdtitle].setdefault(lang, {})
            if lang not in ViewsData[mdtitle].keys():
                ViewsData[mdtitle][lang] = {}
            # ---
            if viws_in > 0 and all_views == 0:
                continue
            # ---
            ViewsData[mdtitle][lang] = {"title": title, "views": all_views}
            # ---
            N_g[1] += 1
            # ---
            if N_g[1] % 100 == 0:
                dump_data(file, ViewsData)


def get_lang_links_mdtitles(lang_links):
    # ---
    lang_links_mdtitles = {lang: {} for mdtitle, tab in lang_links.items() for lang in tab["langs"].keys()}
    # ---
    for lang in lang_links_mdtitles.keys():
        lang_links_mdtitles[lang] = {tab["langs"][lang]: md for md, tab in lang_links.items() if lang in tab["langs"]}
    # ---
    with open(f"{Dir}/lists/lang_links_mdtitles.json", "w", encoding="utf-8") as f:
        json.dump(lang_links_mdtitles, f, ensure_ascii=False, indent=2)
    # ---
    # sort lang_links_mdtitles by length
    lang_links_mdtitles = dict(sorted(lang_links_mdtitles.items(), key=lambda x: len(x[1]), reverse=True))
    # ---
    # print first 10 of lang_links_mdtitles
    to_p = dict(list(lang_links_mdtitles.items())[0:10])
    # ---
    for x, z in to_p.items():
        logger.info(x, len(z))
    # ---
    return lang_links_mdtitles


def start():
    # ---
    with open(f"{Dir}/lists/lang_links.json", "r", encoding="utf-8") as f:
        lang_links = json.load(f)  # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
    # ---
    lang_links_mdtitles = get_lang_links_mdtitles(lang_links)
    # ---
    # len of tab in lang_links
    all_length = sum(len(tab.keys()) for tab in lang_links_mdtitles.values())
    # ---
    to_work = lang_links_mdtitles
    # ---
    n = 0
    # ---
    for lang, tab in to_work.items():
        # ---
        n += 1
        # ---
        ViewsData.update({x: {} for x in tab.values() if x not in ViewsData})
        # ---
        logger.info(f"<<blue>> p:{n}/{all_length} lang: {lang}, titles: {len(tab)}")
        # ---
        get_v(lang, tab, lang_links_mdtitles)
        # ---
    # ---
    dump_data(file, ViewsData)


if __name__ == "__main__":
    start()
