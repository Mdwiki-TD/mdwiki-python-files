#!/usr/bin/python3
"""
بوت قواعد البيانات

python3 core8/pwb.py mdpy/wddone

"""
from mdapi_sql import sql_for_mdwiki
from mdpy.bots import py_tools

que = """
select title,user,lang,target
from pages
where target != ""
;"""
# ---
sq = sql_for_mdwiki.select_md_sql(que)
# ---
for tab in sq:
    mdtitle = py_tools.Decode_bytes(tab[0])
    user = py_tools.Decode_bytes(tab[1])
    lang = py_tools.Decode_bytes(tab[2]).lower()
    target = py_tools.Decode_bytes(tab[3])
    # ---
    done_qu = """
        INSERT INTO wddone (mdtitle, target, lang, user)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1
            FROM wddone
                WHERE mdtitle = %s
                AND lang = %s
                AND user = %s
            )
    """
    # ---
    values = [mdtitle, target, lang, user, mdtitle, lang, user]
    # ---
    print("**************")
    print(done_qu)
    print("**************")
    # ---
    vfg = sql_for_mdwiki.mdwiki_sql(done_qu, update=True, values=values)
# ---
