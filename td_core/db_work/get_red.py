#!/usr/bin/python3
#   himo
"""
اصلاح التحويلات في قواعد البيانات

python3 core8/pwb.py db_work/get_red

"""
import sys
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from mdapi_sql import sql_qids_others
from apis import mdwiki_api

mdwiki_to_qid = sql_for_mdwiki.get_all_qids()
mdtitle_to_qid = sql_qids_others.get_others_qids()


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
    for old_title, new_title in table.items():
        # ---
        new_title_qid = tab.get(new_title, False)
        old_title_qid = tab.get(old_title, False)
        # ---
        if not old_title_qid:
            continue
        # ---
        if not new_title_qid:
            # استبدال
            # ---
            set_new_title[new_title] = old_title_qid
            # ---
            tat += f'old_title: "{old_title}" to: "{new_title}",\n'
            # ---
        elif new_title_qid == old_title_qid:
            to_del.append(old_title)
    # ---
    printe.output("===================")
    if tat != "":
        printe.output("<<red>> redirects: ")
        printe.output(tat)
        printe.output("===================")
    # ---
    printe.output(f"len set_new_title {len(set_new_title)}.")
    # ---
    printe.output(f"len to_del {len(to_del)}: \n" + "\n\t".join(to_del))
    # ---
    if "no" not in sys.argv:
        if set_new_title:
            # ---
            for new_title, old_title_qid in set_new_title.items():
                sql_for_mdwiki.set_title_where_qid(new_title, old_title_qid)
            # ---
            sql_for_mdwiki.add_titles_to_qids(set_new_title)


if __name__ == "__main__":
    get_pages(mdwiki_to_qid)
    get_pages(mdtitle_to_qid)
