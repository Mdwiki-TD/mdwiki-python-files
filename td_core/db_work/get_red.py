#!/usr/bin/python3
#   himo
"""
اصلاح التحويلات في قواعد البيانات

python3 core8/pwb.py db_work/get_red

"""
import logging
import sys

from apis import mdwiki_api
from mdapi_sql import sql_for_mdwiki, sql_qids_others

logger = logging.getLogger(__name__)

# mdwiki_api.api_new.Login_to_wiki()

qids_title_to_qid = sql_for_mdwiki.get_all_qids()
qids_others_title_to_qid = sql_qids_others.get_others_qids()


def get_table(titles):
    table = {}
    # ---
    done = 0
    # ---
    len_grup = 100
    # ---
    for i in range(0, len(titles), len_grup):
        group = titles[i : i + len_grup]
        # ---
        done += len(group)
        # ---
        asa = mdwiki_api.get_redirect(group)
        # ---
        print(f"work on {len_grup} pagees, done: {done}/{len(titles)}.")
        # ---
        table = {**table, **asa}
    # ---
    print(f"len of table {len(table)} ")
    # ---
    return table


def get_pages(tab):
    # ---
    titles = list(tab.keys())
    # ---
    table = get_table(titles)
    # ---
    tat = ""
    # ---
    set_new_title = {}
    to_del = []
    # ---
    just_test = "no" in sys.argv
    # ---
    for old_title, new_title in table.items():
        # ---
        new_qid = tab.get(new_title, False)
        old_qid = tab.get(old_title, False)
        # ---
        if not old_qid:
            continue
        # ---
        if not new_qid:
            # استبدال
            # ---
            if qids_title_to_qid.get(old_title):
                sql_for_mdwiki.qids_set_title_where_title_qid(old_title, new_title, old_qid, no_do=just_test)
            # ---
            if qids_others_title_to_qid.get(old_title):
                sql_qids_others.qids_set_title_where_title_qid(old_title, new_title, old_qid, no_do=just_test)
            # ---
            tat += f'old_title: "{old_title}" to: "{new_title}",\n'
            # ---
            set_new_title[new_title] = old_qid
            # ---
        elif new_qid == old_qid:
            to_del.append(old_title)
    # ---
    logger.info(f"len to_del {len(to_del)}: \n" + "\n\t".join(to_del))
    # ---
    old_way = False
    # ---
    if old_way:
        logger.info("===================")
        if tat != "":
            logger.info("<<red>> redirects: ")
            logger.info(tat)
            logger.info("===================")
        # ---
        logger.info(f"len set_new_title {len(set_new_title)}.")
        # ---
        if "no" not in sys.argv:
            if set_new_title:
                # ---
                for new_title, old_qid in set_new_title.items():
                    sql_for_mdwiki.set_title_where_qid(new_title, old_qid)
                # ---
                sql_for_mdwiki.add_titles_to_qids(set_new_title)


def start():
    get_pages(qids_title_to_qid)

    if "nothers" not in sys.argv:
        get_pages(qids_others_title_to_qid)


if __name__ == "__main__":
    start()
