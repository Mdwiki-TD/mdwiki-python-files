#!/usr/bin/python3
"""

إنشاء قائمة بعدد الكلمات

وحفظها في paths.json_tables_path
+
قاعدة البيانات

python3 c9/pwb.py td_core/mdcount/words newpages
python3 c9/pwb.py td_core/mdcount/words
python3 c9/pwb.py td_core/mdcount/words listnew

python3 c9/pwb.py td_core/mdcount/words more400

python3 c9/pwb.py td_core/mdcount/words less100
python3 c9/pwb.py td_core/mdcount/words sql

USED IN mdwiki-jobs.yaml
"""

import logging
import sys

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.apis import mdwiki_api_call
from td_core.mdcount.bots import lead
from td_core.mdcount.bots.links import get_links_from_cats
from td_core.mdcount.ref_words_bot import do_to_sql, get_jsons_new, logaa, make_old_values
from td_core.td_dirs import paths

logger = logging.getLogger(__name__)

tab_data = {"all": {}, "lead": {}}

file_all = paths.json_files.allwords
file_lead = paths.json_files.words


def start_to_sql():
    return do_to_sql(tab_data["all"], tab_data["lead"], ty="word")


def count_words(title) -> None:

    text = mdwiki_api_call.get_page_text(title)

    lead_c, all_c = lead.count_all(title="", text=text)

    tab_data["all"][title] = all_c
    tab_data["lead"][title] = lead_c

    logger.info(f"<<green>> all:{all_c} \t lead:{lead_c}")


def from_sql(old_values):

    # Migrated from `all_articles` (single-category-per-article) to
    # `category_members` (many-to-many). DISTINCT collapses the duplicates
    # introduced when an article belongs to multiple categories.
    que = """select DISTINCT article_id from category_members;"""

    sq = sql_for_mdwiki.mdwiki_sql_dict(que)

    titles2 = [q["article_id"] for q in sq]

    titles = [x for x in titles2 if x not in old_values]

    logger.info(f"<<yellow>> sql: find {len(titles2)} titles, {len(titles)} to work. ")

    return titles


def get_links(ty: str = "ref"):

    titles = []

    old_values = make_old_values(tab_data["all"], tab_data["lead"])

    if "sql" in sys.argv:
        titles = from_sql(old_values)
    else:
        titles = get_links_from_cats()

    if "newpages" in sys.argv:
        titles = [x for x in titles if (x not in old_values)]

    return titles


def main() -> None:

    tab_data["all"], tab_data["lead"] = get_jsons_new(file_all, file_lead, "word")

    limit = 100 if "limit100" in sys.argv else 10000

    # python3 c9/pwb.py td_core/mdcount/countref -title:Testosterone_\(medication\)

    vaild_links = []

    for arg in sys.argv:
        arg, _, value = arg.partition(":")

        if arg == "-title":
            vaild_links = [value.replace("_", " ")]

    if not vaild_links:
        vaild_links = get_links()

    for numb, x in enumerate(vaild_links):
        x = x.replace("\\'", "'")

        logger.info("------------------")
        logger.info(f"page {numb} from {len(vaild_links)}, x:{x}")

        if numb >= limit:
            break

        count_words(x)

        # if numb == 10 or str(numb).endswith("00"):
        #     logaa(file_lead, tab_data["lead"])
        #     logaa(file_all, tab_data["all"])

    logaa(file_lead, tab_data["lead"])
    logaa(file_all, tab_data["all"])

    start_to_sql()


if __name__ == "__main__":
    main()

    if "sql" not in sys.argv:
        sys.argv.append("sql")

        main()
