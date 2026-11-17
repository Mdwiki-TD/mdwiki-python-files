#!/usr/bin/python3
"""
إنشاء قائمة بعدد المراجع والكلمات وحفظها في قاعدة البيانات

python3 c9/pwb.py td_core/mdcount/countrefs_and_words newpages

python3 c9/pwb.py td_core/mdcount/countrefs_and_words -title:Esophageal_rupture

USED IN mdwiki-jobs.yaml
"""

import logging
import sys

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.apis import mdwiki_api_call
from td_core.mdcount.bots.lead import count_all
from td_core.mdcount.bots.countref_bots import count_ref_from_text
from db.to_sql_new import new_to_sql


logger = logging.getLogger(__name__)

refs_tab_data = {"all": {}, "lead": {}}
words_tab_data = {"all": {}, "lead": {}}


def get_table_and_columns(ty):
    if ty == "ref":
        table = "refs_counts"
        title_c = "r_title"
        all_c = "r_all_refs"
        lead_c = "r_lead_refs"
    elif ty == "word":
        table = "words"
        title_c = "w_title"
        all_c = "w_all_words"
        lead_c = "w_lead_words"
    else:
        logger.exception("Unknown type %s", ty)
        raise ValueError(f"Unknown type {ty}")

    return table, title_c, all_c, lead_c


def do_to_sql(data_all, data_lead, ty: str = "ref") -> None:
    table, title_c, all_c, lead_c = get_table_and_columns(ty)

    data2 = [{title_c: x, lead_c: v, all_c: data_all.get(x, 0)} for x, v in data_lead.items()]

    new_to_sql(
        data=data2,
        table_name=table,
        columns=[title_c, lead_c, all_c],
        title_columns=[title_c],
    )


def get_jsons_new(ty):

    table, title_c, all_c, lead_c = get_table_and_columns(ty)

    in_sql = sql_for_mdwiki.mdwiki_sql_dict(f"select DISTINCT {title_c}, {lead_c}, {all_c} from {table}")

    all_data = {x[title_c]: x[all_c] for x in in_sql}

    lead_data = {x[title_c]: x[lead_c] for x in in_sql}

    logger.info(f"len of lead_data:{len(lead_data.keys())}, all :{len(all_data.keys())}")

    # sort lead_data by name
    lead_data = {k: lead_data[k] for k in sorted(lead_data)}
    all_data = {k: all_data[k] for k in sorted(all_data)}

    return all_data, lead_data


def count_words(title, text: str) -> None:

    lead_c, all_c = count_all(title="", text=text)

    words_tab_data["all"][title] = all_c
    words_tab_data["lead"][title] = lead_c

    logger.info(f"<<green>> all:{all_c} \t lead:{lead_c}")


def count_refs(title, text: str) -> None:

    text2 = text

    all_c = count_ref_from_text(text2)

    leadtext = text2.split("==")[0]
    lead_c = count_ref_from_text(leadtext, get_short=True)

    refs_tab_data["all"][title] = all_c
    refs_tab_data["lead"][title] = lead_c

    logger.info(f"<<green>> all:{all_c} \t lead:{lead_c}")


def from_sql():
    que = """select DISTINCT article_id from category_members;"""

    sq = sql_for_mdwiki.mdwiki_sql_dict(que)

    titles2 = [q["article_id"] for q in sq]

    logger.info(f"<<yellow>> sql: find {len(titles2)} titles")

    return titles2


def main() -> None:

    words_tab_data["all"], words_tab_data["lead"] = get_jsons_new("word")

    refs_tab_data["all"], refs_tab_data["lead"] = get_jsons_new("ref")

    vaild_links = from_sql()

    for numb, x in enumerate(vaild_links):
        x = x.replace("\\'", "'")

        logger.info("------------------")
        logger.info(f"page {numb} from {len(vaild_links)}, x:{x}")

        text = mdwiki_api_call.get_page_text(x)

        count_words(x, text)
        count_refs(x, text)

    do_to_sql(
        words_tab_data["all"],
        words_tab_data["lead"],
        ty="word",
    )

    do_to_sql(
        refs_tab_data["all"],
        refs_tab_data["lead"],
        ty="ref",
    )


if __name__ == "__main__":
    main()

    if "sql" not in sys.argv:
        sys.argv.append("sql")

        main()
