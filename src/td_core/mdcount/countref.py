#!/usr/bin/python3
"""

إنشاء قائمة بعدد المراجع

وحفظها في paths.json_tables_path
+
قاعدة البيانات


python3 core8/pwb.py td_core/mdcount/countref merge
python3 core8/pwb.py td_core/mdcount/countref newpages

python3 core8/pwb.py td_core/mdcount/countref -title:Esophageal_rupture

"""

import json
import logging
import sys

from db.mdapi_sql import sql_for_mdwiki
from md_core_helps.apis import mdwiki_api_call
from td_core.mdcount.bots.countref_bots import count_ref_from_text
from td_core.mdcount.bots.links import get_links_from_cats
from td_core.mdcount.ref_words_bot import do_to_sql, get_jsons_new, logaa, make_old_values
from td_core.td_dirs import paths

logger = logging.getLogger(__name__)


# ---
tab_data = {"all": {}, "lead": {}}
# ---s


def start_to_sql():
    return do_to_sql(tab_data["all"], tab_data["lead"], ty="ref")


def count_refs(title) -> None:
    # ---
    text = mdwiki_api_call.GetPageText(title)
    # ---
    # extend short refs
    text2 = text
    # text2 = ref.fix_ref(text, text)
    # ---
    all_c = count_ref_from_text(text2)
    # ---
    leadtext = text2.split("==")[0]
    lead_c = count_ref_from_text(leadtext, get_short=True)
    # ---
    tab_data["all"][title] = all_c
    tab_data["lead"][title] = lead_c
    # ---
    logger.info(f"<<green>> all:{all_c} \t lead:{lead_c}")


def from_sql(old_values):
    # ---
    # Migrated from `all_articles` (single-category-per-article) to
    # `category_members` (many-to-many). DISTINCT collapses the duplicates
    # introduced when an article belongs to multiple categories.
    que = """select DISTINCT article_id from category_members;"""
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    titles2 = [q["article_id"] for q in sq]
    # ---
    titles = [x for x in titles2 if x not in old_values]
    # ---
    logger.info(f"<<yellow>> sql: find {len(titles2)} titles, {len(titles)} to work. ")
    # ---
    return titles


def get_links(ty: str = "ref"):
    # ---
    titles = []
    # ---
    old_values = make_old_values(tab_data["all"], tab_data["lead"])
    # ---
    if "sql" in sys.argv:
        titles = from_sql(old_values)
    else:
        titles = get_links_from_cats()
    # ---
    if "newpages" in sys.argv:
        titles = [x for x in titles if (x not in old_values)]
    # ---
    return titles


def main() -> None:
    # ---
    tab_data["all"], tab_data["lead"] = get_jsons_new(
        paths.json_files.all_refcount, paths.json_files.lead_refcount, "ref"
    )
    # ---
    if "merge" in sys.argv:
        # ---
        with open(paths.json_files.all_refcount, "w", encoding="utf-8") as outfile:
            logger.info(f"<<green>> {len(tab_data['all'])} lines to {paths.json_files.all_refcount}")
            json.dump(tab_data["all"], outfile, sort_keys=True, indent=2)
        # ---
        with open(paths.json_files.lead_refcount, "w", encoding="utf-8") as outfile:
            logger.info(f"<<green>> {len(tab_data['lead'])} lines to {paths.json_files.lead_refcount}")
            json.dump(tab_data["lead"], outfile, sort_keys=True, indent=2)
        # ---
        start_to_sql()
        # ---
        exit()
    # ---
    limit = 100 if "limit100" in sys.argv else 10000
    # ---
    # python3 core8/pwb.py td_core/mdcount/countref -title:Testosterone_\(medication\)
    # ---
    vaild_links = []
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg == "-title":
            vaild_links = [value.replace("_", " ")]
    # ---
    if not vaild_links:
        vaild_links = get_links()
    # ---
    for numb, x in enumerate(vaild_links):
        # ---
        x = x.replace("\\'", "'")
        # ---
        logger.info("------------------")
        logger.info(f"page {numb} from {len(vaild_links)}, x:{x}")
        # ---
        if numb >= limit:
            break
        # ---
        count_refs(x)
        # ---
        # if numb == 10 or str(numb).endswith("00"):
        #     logaa(paths.json_files.lead_refcount, tab_data["lead"])
        #     logaa(paths.json_files.all_refcount, tab_data["all"])
    # ---
    logaa(paths.json_files.lead_refcount, tab_data["lead"])
    logaa(paths.json_files.all_refcount, tab_data["all"])
    # ---
    start_to_sql()


def test() -> None:
    # python3 core8/pwb.py td_core/mdcount/countref test
    # ---
    tab_data["lead"]["Yemen1"] = 50
    tab_data["all"]["Yemen1"] = 50
    # ---
    tab_data["lead"]["Sana'a"] = 500
    tab_data["all"]["Sana'a"] = 100
    # ---
    start_to_sql()


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
        exit()
    # ---
    main()
    # ---
    if "sql" not in sys.argv:
        sys.argv.append("sql")
        # ---
        main()
