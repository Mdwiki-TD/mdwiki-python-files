#!/usr/bin/python3
"""

بوت قواعد البيانات
from api_sql import sql

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys
import re
import time as tttime
import datetime
from datetime import datetime
from pymysql.converters import escape_string

# ---
from API import printe
from api_sql import sql_qu

# ---
can_use_sql_db = sql_qu.can_use_sql_db
db_username = sql_qu.db_username
# ---
# ar_site = pywikibot.Site('ar' , "wikipedia")
# ---
ns_text_tab_1 = {
    1: "نقاش",
    2: "مستخدم",
    3: "نقاش المستخدم",
    4: "ويكيبيديا",
    5: "نقاش ويكيبيديا",
    6: "ملف",
    7: "نقاش الملف",
    10: "قالب",
    11: "نقاش القالب",
    12: "مساعدة",
    13: "نقاش المساعدة",
    14: "تصنيف",
    15: "نقاش التصنيف",
    100: "بوابة",
    101: "نقاش البوابة",
    828: "وحدة",
    829: "نقاش الوحدة",
}
ns_text_tab = {}
# ---
for ns, title in ns_text_tab_1.items():
    ns_text_tab[ns] = title
    ns_text_tab[str(ns)] = title


def GET_SQL():
    if 'nosql' in sys.argv:
        return False
    # ---
    print(f'GET_SQL() == {can_use_sql_db[1]}')
    # ---
    return can_use_sql_db[1]


def Decode_bytes(x):
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    return x


def make_labsdb_dbs_p(wiki):  # host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    if wiki.endswith('wiki'):
        wiki = wiki[:-4]
    # ---
    wiki = wiki.replace("-", "_")
    # ---
    databases = {
        "be-x-old": "be_x_old",
        "be_tarask": "be_x_old",
        "be-tarask": "be_x_old",
    }
    # ---
    wiki = databases.get(wiki, wiki)
    # ---
    wiki = f"{wiki}wiki"
    # ---
    dbs = wiki
    # ---
    host = f"{wiki}.analytics.db.svc.wikimedia.cloud"
    # ---
    dbs_p = f'{dbs}_p'
    # ---
    return host, dbs_p


def make_sql_connect(query, db='', host='', update=False, Return=False, return_dict=False):
    return sql_qu.make_sql_connect(
        query,
        db=db,
        host=host,
        update=update,
        Return=Return,
        return_dict=return_dict,
    )


def MySQLdbar(arcatTitle):
    # ---
    arcats = []
    # ---
    if not GET_SQL():
        return arcats
    # ---
    arcatTitle = re.sub(r'تصنيف:', '', arcatTitle)
    arcatTitle = re.sub(r' ', '_', arcatTitle)
    print(f"arcatTitle : {arcatTitle}")
    # ---
    arcatTitle = escape_string(arcatTitle)
    # ---
    ar_queries = f'''
        SELECT page_title, page_namespace
        FROM page
        JOIN categorylinks
        JOIN langlinks
        WHERE cl_to = "{arcatTitle}"
        AND cl_from = page_id
        AND page_id = ll_from
        AND ll_lang = "en"
        GROUP BY page_title ;'''
    # ---
    host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    ar_results = make_sql_connect(ar_queries, db=dbs_p, host=host, Return=[], return_dict=True)
    # ---
    if not ar_results or len(ar_results) == 0:
        return arcats
    # ---
    for ra in ar_results:
        # ---
        title = ra['page_title']
        title = re.sub(r' ', '_', title)
        # ---
        ns = ra['page_namespace']
        # ---
        if ns_text_tab.get(ns):
            title = f"{ns_text_tab.get( ns )}:{title}"
        # ---
        arcats.append(str(title))
        # ---
    # ---
    print(f"arcats: {len(arcats)} {arcatTitle}")
    # ---
    return arcats


def Make_sql(queries, wiki="", printqua=False):
    encats = []
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    if not GET_SQL():
        return encats
    # ---
    if not wiki:
        wiki = "enwiki"
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    if printqua:
        print(queries)
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    printe.output(f'<<lightred>> API/sql_py Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return=[])
    final = tttime.time()
    # ---end of sql--------------------------------------------
    for raw in en_results:
        tit = Decode_bytes(raw[0])
        tit = re.sub(r' ', '_', tit)
        encats.append(tit)
    # ---
    delta = int(final - start)
    # ---
    print(f'API/sql_py Make_sql len(encats) = "{len( encats )}", in {delta} seconds')
    # ---
    encats.sort()
    # ---
    return encats


def Make_sql_many_rows(queries, wiki="", printqua=False):
    rows = []
    # ---
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    print(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if not GET_SQL():
        return rows
    # ---
    if printqua:
        print(queries)
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    printe.output(f'<<lightred>> API/sql_py Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return={})
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        # if type(raw) == bytes:
        # raw = raw.decode("utf-8")
        raw2 = raw
        # if type(raw2) == list or type(raw2) == tuple :
        if isinstance(raw2, list):
            raw = [Decode_bytes(x) for x in raw2]
        rows.append(raw)
    # ---
    delta = int(final - start)
    print(f'API/sql_py Make_sql_many_rows len(encats) = "{len( rows )}", in {delta} seconds')
    # ---
    return rows


def Make_sql_2_rows(queries, wiki="", printqua=False):
    # ---
    encats = {}
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    print(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        print(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    printe.output(f'<<lightred>> API/sql_py Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return={})
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        key = Decode_bytes(raw[0])
        value = Decode_bytes(raw[1])
        # ---
        encats[key] = value
    # ---
    delta = int(final - start)
    print(f'API/sql_py Make_sql_2_rows len(results) = "{len( encats )}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_rows(queries, wiki="", printqua=False):
    encats = []
    # ---
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    print(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        print(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    printe.output(f'<<lightred>> API/sql_py Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return=[])
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        en = Decode_bytes(raw[0])
        encats.append(en)
    # ---
    delta = int(final - start)
    print(f'API/sql_py Make_sql_2_rows len(results) = "{len( encats )}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_row(queries, wiki="", printqua=False):
    return Make_sql_1_rows(queries, wiki=wiki, printqua=printqua)


def MySQLdb_finder_2_rows(encatTitle):
    # en category use template with ar link
    printe.output(f'<<lightred>> sql . MySQLdb_finder_2_rows {encatTitle}: ')
    # ---
    if not GET_SQL():
        return {}
    # ---
    item = encatTitle.replace(' ', '_')
    item = str(encatTitle).replace(' ', '_')
    # ---start sql---------------------------------------
    queries = '''
    select CONCAT("Category:",page_title), ll_title
    from page, templatelinks, langlinks
    where page_id = tl_from
    AND page_namespace = 14
    AND ll_lang = "ar"
    AND ll_from = page_id

    AND tl_target_id = (SELECT lt_id FROM linktarget WHERE lt_namespace = 10 AND lt_title = "%s")
    '''
    queries %= item
    encats = Make_sql_2_rows(queries)
    # ---end of sql--------------------------------------------
    printe.output(f"encats: <<lightred>> {len(encats.keys())} <<default>> template:{item}")
    # ---
    return encats


def MySQLdb_finder_N_New(encatTitle, arcatTitle):
    printe.output(f'<<lightred>> sql . MySQLdb_finder {encatTitle}: ')
    # ---
    item = encatTitle.replace('category:', '').replace('Category:', '').replace(' ', '_')
    item = str(encatTitle).replace('[[en:', '').replace(']]', '').replace(' ', '_').replace('Category:', '')
    # ---
    if not GET_SQL():
        return False
    # ---
    start = tttime.time()
    # ---
    item = escape_string(item)
    # ---
    queries = f'''SELECT /* SLOW_OK */ ll_title , page_namespace  FROM page JOIN categorylinks JOIN langlinks
        WHERE cl_to = "{item}" AND cl_from=page_id AND page_id =ll_from AND ll_lang = "ar"
        GROUP BY ll_title ;'''
    # ---
    encats = Make_sql(queries)
    arcats = MySQLdbar(arcatTitle) if arcatTitle and arcatTitle != "" else []
    # ---
    final = tttime.time()
    printe.output(f"encats: <<lightred>> {len(encats)} <<default>> {item}")
    final_cat = [str(cat) for cat in encats if cat not in arcats]
    # ---
    delta = int(final - start)
    print(f'API/sql_py MySQLdb_finder_N_New len(final_cat) = "{len( final_cat )}", in {delta} seconds')
    # ---
    return final_cat if final_cat != [] else False


def MySQLdb_finder_New(encatTitle, arcatTitle):
    printe.output(f'<<lightred>> API/sql_py MySQLdb_finder_New {encatTitle}: ')
    # ---
    return MySQLdb_finder_N_New(encatTitle, arcatTitle)


if __name__ == '__main__':
    # ---
    arqueries = '''
        select CONCAT("تصنيف:",page_title), ll_title
        from page, templatelinks, langlinks
        where page_id = tl_from
        AND page_namespace = 14
        AND ll_lang = "en"
        AND ll_from = page_id
        AND tl_target_id = (SELECT lt_id FROM linktarget WHERE lt_namespace = 10 AND lt_title = "أشخاص_حسب_المهنة")
        '''
    # ---
    ss = Make_sql_2_rows(arqueries, wiki="arwiki")
    # ss = MySQLdb_finder_2_rows("Fooian_fooers")
    printe.output(f'sql py test:: Make_sql_2_rows lenth:{len(ss)}')
