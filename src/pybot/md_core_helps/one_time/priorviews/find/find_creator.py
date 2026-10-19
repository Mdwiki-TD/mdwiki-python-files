"""

python3 core8/pwb.py priorviews/find/find_creator new
python3 core8/pwb.py priorviews/find/find_creator -lang:ar

"""

import json

# ---
import logging
import os
import sys
from pathlib import Path

from pymysql.converters import escape_string

from db import WikiReplicaDB
from md_core_helps.one_time.priorviews.bots import helps
from md_core_helps.one_time.priorviews.lists.links_by_section import links_by_lang

logger = logging.getLogger(__name__)


added = 0

Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f"{Dir2}/lists/creators_by_lang.json"
# ---
if not os.path.exists(file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump({}, f)
# ---
CreatorsData = json.load(open(file, "r", encoding="utf-8"))


def log_data() -> None:
    logger.info(f"<<yellow>> {len(CreatorsData)} CreatorsData")
    # dump CreatorsData
    helps.dump_data(file, CreatorsData)


def get_creator(links, lang) -> None:
    global added
    # ---
    if lang not in CreatorsData:
        CreatorsData[lang] = {}

    def valid(x, tab, empty: str = "") -> bool:
        i = tab.get(x) or tab.get(x.lower())
        if not i or i == empty:
            return True
        return False

    # ---
    if "new" in sys.argv:
        # links = [ x for x in links if not x in CreatorsData[lang] or CreatorsData[lang][x] == '']
        links = [x for x in links if valid(x, CreatorsData[lang])]
    # ---
    logger.info(f"lang: {lang}, links: {len(links)}")
    # ---
    if len(links) == 0:
        return
    # ---
    # split links to 100 per group
    for i in range(0, len(links), 100):
        titles = [x.replace(" ", "_") for x in links[i : i + 100]]
        # ---
        titles = ", ".join([f'"{escape_string(x)}"' for x in titles])
        # ---
        query = f"""select rev_timestamp, page_title, actor_name, comment_text
            from revision, actor, page, comment
            where actor_id = rev_actor
            and rev_parent_id = 0
            and page_id = rev_page
            and page_namespace = 0
            and rev_comment_id = comment_id
            and page_title in ({titles})
        """
        # ---
        lang_db = WikiReplicaDB(lang)
        result = lang_db.select_safe(query)
        # ---
        for x in result:
            time_stamp = int(x["rev_timestamp"])
            page_title = x["page_title"].replace("_", " ")
            actor_name = x["actor_name"].replace("_", " ")
            comment_text = x["comment_text"]
            # ---
            z_id = False
            # ---
            if comment_text.find("|User:Mr. Ibrahem/") != -1:
                z_id = True
            # ---
            logger.info(f"time:{time_stamp} title:{page_title} actor:{actor_name}")
            # ---
            tab = {"time": time_stamp, "actor": actor_name, "comment": comment_text, "TD": z_id}
            # ---
            added += 1
            # ---
            CreatorsData[lang][page_title] = tab
            # ---
            if added % 50 == 0:
                log_data()
            # ---
        # ---
        if "testt" in sys.argv:
            logger.info(result)
            break


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
    for lang in langkeys:
        # ---
        links = links_by_lang[lang]
        # ---
        n += 1
        # ---
        get_creator(links, lang)
        # ---
    # ---
    log_data()

    # ---


if __name__ == "__main__":
    start()
