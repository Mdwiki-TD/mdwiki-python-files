#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/sql_for_mdwiki_new

# ---
from mdapi_sql import sql_for_mdwiki_new
# sql_for_mdwiki_new. select_md_sql(query, return_dict=False, values=None)
# sql_for_mdwiki_new. mdwiki_sql(query, return_dict=False, values=None, many=False)
# sql_for_mdwiki_new. mdwiki_sql_dict(query, values=None, many=False)
# ---
(all_exists|all_articles|all_qids_exists|all_articles_titles|all_qids|all_qids_titles)
"""
from mdapi_sql import sql_td_bot


def mdwiki_sql(query, return_dict=False, values=None, many=False, **kwargs):
    # ---
    if not query:
        print("query == ''")
        return {}
    # ---
    return sql_td_bot.sql_connect_mdwiki_new(query, return_dict=return_dict, values=values, many=many, **kwargs)


def mdwiki_sql_dict(query, values=None, many=False, **kwargs):
    # ---
    if not query:
        print("query == ''")
        return {}
    # ---
    return sql_td_bot.sql_connect_mdwiki_new(query, return_dict=True, values=values, many=many, **kwargs)


def select_md_sql(query, *args, **kwargs):
    # ---
    if not query:
        print("query == ''")
        return {}
    # ---
    return mdwiki_sql(query, *args, **kwargs)


if __name__ == "__main__":
    # python3 core8/pwb.py md_core_helps/mdapi_sql/sql_for_mdwiki_new
    # d = add_qid("Zolpidem", "Q218842")
    d = ("Zolpidem", "Q218842")
    print(f"{len(d)=}")
