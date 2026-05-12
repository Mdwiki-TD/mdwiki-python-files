#!/usr/bin/python3
"""

بوت قواعد البيانات
from mdapi_sql import sql

"""
import logging
import re
import sys
import time as tttime
from datetime import datetime

from mdapi_sql import sql_qu
from pymysql.converters import escape_string

logger = logging.getLogger(__name__)
# ---
can_use_sql_db = sql_qu.can_use_sql_db
db_username = sql_qu.db_username

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
    if "nosql" in sys.argv:
        return False
    # ---
    logger.info(f"GET_SQL() == {can_use_sql_db[1]}")
    # ---
    return can_use_sql_db[1]


def Decode_bytes(x):
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    return x


def make_labsdb_dbs_p(wiki):  # host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    pre_defined_db_mapping = {
        "gsw": "alswiki_p",
        "sgs": "bat_smgwiki_p",
        "bat-smg": "bat_smgwiki_p",
        "be-tarask": "be_x_oldwiki_p",
        "bho": "bhwiki_p",
        "cbk": "cbk_zamwiki_p",
        "cbk-zam": "cbk_zamwiki_p",
        "vro": "fiu_vrowiki_p",
        "fiu-vro": "fiu_vrowiki_p",
        "map-bms": "map_bmswiki_p",
        "nds-nl": "nds_nlwiki_p",
        "nb": "nowiki_p",
        "rup": "roa_rupwiki_p",
        "roa-rup": "roa_rupwiki_p",
        "roa-tara": "roa_tarawiki_p",
        "lzh": "zh_classicalwiki_p",
        "zh-classical": "zh_classicalwiki_p",
        "nan": "zh_min_nanwiki_p",
        "zh-min-nan": "zh_min_nanwiki_p",
        "yue": "zh_yuewiki_p",
        "zh-yue": "zh_yuewiki_p",
    }
    # ---
    wiki_normalized = wiki.strip().lower().removesuffix("_p").removesuffix("wiki")
    if wiki_normalized in pre_defined_db_mapping:
        dbs_p = f"{pre_defined_db_mapping[wiki_normalized]}"
        sub_host = dbs_p.removesuffix("_p")
        host = f"{sub_host}.analytics.db.svc.wikimedia.cloud"
        return host, dbs_p
    # ---
    wiki = wiki.removesuffix("wiki")
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
    dbs_p = f"{dbs}_p"
    # ---
    return host, dbs_p


def make_sql_connect(query, db="", host="", update=False, _return=False, return_dict=False):
    return sql_qu.make_sql_connect(
        query,
        db=db,
        host=host,
        update=update,
        _return=_return,
        return_dict=return_dict,
    )


def fetch_arcat_titles(arcat_title):
    # ---
    arcats = []
    # ---
    if not GET_SQL():
        return arcats
    # ---
    arcat_title = re.sub(r"تصنيف:", "", arcat_title)
    arcat_title = re.sub(r" ", "_", arcat_title)
    logger.info(f"arcat_title : {arcat_title}")
    # ---
    arcat_title = escape_string(arcat_title)
    # ---
    ar_queries = f"""
        SELECT page_title, page_namespace
        FROM page
        JOIN categorylinks
        JOIN langlinks
        WHERE cl_to = "{arcat_title}"
        AND cl_from = page_id
        AND page_id = ll_from
        AND ll_lang = "en"
        GROUP BY page_title ;"""
    # ---
    host, dbs_p = make_labsdb_dbs_p("ar")
    # ---
    ar_results = make_sql_connect(ar_queries, db=dbs_p, host=host, _return=[], return_dict=True)
    # ---
    if not ar_results or len(ar_results) == 0:
        return arcats
    # ---
    for ra in ar_results:
        # ---
        title = ra["page_title"]
        title = re.sub(r" ", "_", title)
        # ---
        ns = ra["page_namespace"]
        # ---
        if ns_text_tab.get(ns):
            title = f"{ns_text_tab.get(ns)}:{title}"
        # ---
        arcats.append(str(title))
        # ---
    # ---
    logger.info(f"arcats: {len(arcats)} {arcat_title}")
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
        logger.info(queries)
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.info(f'<<red>> db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, _return=[])
    final = tttime.time()
    # ---end of sql--------------------------------------------
    for raw in en_results:
        tit = Decode_bytes(raw[0])
        tit = re.sub(r" ", "_", tit)
        encats.append(tit)
    # ---
    delta = int(final - start)
    # ---
    logger.info(f'Make_sql len(encats) = "{len(encats)}", in {delta} seconds')
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
    logger.info(f"Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if not GET_SQL():
        return rows
    # ---
    if printqua:
        logger.info(queries)
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.info(f'<<red>> Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, _return={})
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
    logger.info(f'Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    # ---
    return rows


def Make_sql_2_rows(queries, wiki="", printqua=False):
    # ---
    encats = {}
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    logger.info(f"Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        logger.info(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.info(f'<<red>> Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, _return={})
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
    logger.info(f'Make_sql_2_rows len(results) = "{len(encats)}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_rows(queries, wiki="", printqua=False):
    encats = []
    # ---
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    logger.info(f"Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        logger.info(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.info(f'<<red>> Make_sql db:"{dbs_p}", db_username:"{db_username}" {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, _return=[])
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        en = Decode_bytes(raw[0])
        encats.append(en)
    # ---
    delta = int(final - start)
    logger.info(f'Make_sql_2_rows len(results) = "{len(encats)}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_row(queries, wiki="", printqua=False):
    return Make_sql_1_rows(queries, wiki=wiki, printqua=printqua)


def MySQLdb_finder_2_rows(encat_title):
    # en category use template with ar link
    logger.error(f"<<red>> sql . {encat_title}: ")
    # ---
    if not GET_SQL():
        return {}
    # ---
    item = encat_title.replace(" ", "_")
    item = str(encat_title).replace(" ", "_")
    # ---start sql---------------------------------------
    queries = """
    select CONCAT("Category:",page_title), ll_title
    from page, templatelinks, langlinks
    where page_id = tl_from
    AND page_namespace = 14
    AND ll_lang = "ar"
    AND ll_from = page_id

    AND tl_target_id = (SELECT lt_id FROM linktarget WHERE lt_namespace = 10 AND lt_title = "%s")
    """
    queries %= item
    encats = Make_sql_2_rows(queries)
    # ---end of sql--------------------------------------------
    logger.info(f"encats: <<red>> {len(encats.keys())} <<default>> template:{item}")
    # ---
    return encats


def MySQLdb_finder_N_New(encat_title, arcat_title):
    logger.error(f"<<red>> sql . MySQLdb_finder {encat_title}: ")
    # ---
    item = encat_title.replace("category:", "").replace("Category:", "").replace(" ", "_")
    item = str(encat_title).replace("[[en:", "").replace("]]", "").replace(" ", "_").replace("Category:", "")
    # ---
    if not GET_SQL():
        return False
    # ---
    start = tttime.time()
    # ---
    item = escape_string(item)
    # ---
    queries = f"""SELECT /* SLOW_OK */ ll_title , page_namespace  FROM page JOIN categorylinks JOIN langlinks
        WHERE cl_to = "{item}" AND cl_from=page_id AND page_id =ll_from AND ll_lang = "ar"
        GROUP BY ll_title ;"""
    # ---
    encats = Make_sql(queries)
    arcats = fetch_arcat_titles(arcat_title) if arcat_title and arcat_title != "" else []
    # ---
    final = tttime.time()
    logger.info(f"encats: <<red>> {len(encats)} <<default>> {item}")
    final_cat = [str(cat) for cat in encats if cat not in arcats]
    # ---
    delta = int(final - start)
    logger.info(f'MySQLdb_finder_N_New len(final_cat) = "{len(final_cat)}", in {delta} seconds')
    # ---
    return final_cat if final_cat != [] else False


def get_exclusive_category_titles(encat_title, arcat_title):
    logger.error(f"<<red>> {encat_title}: ")
    # ---
    return MySQLdb_finder_N_New(encat_title, arcat_title)


if __name__ == "__main__":
    # ---
    arqueries = """
        select CONCAT("تصنيف:",page_title), ll_title
        from page, templatelinks, langlinks
        where page_id = tl_from
        AND page_namespace = 14
        AND ll_lang = "en"
        AND ll_from = page_id
        AND tl_target_id = (SELECT lt_id FROM linktarget WHERE lt_namespace = 10 AND lt_title = "أشخاص_حسب_المهنة")
        """
    # ---
    ss = Make_sql_2_rows(arqueries, wiki="arwiki")
    # ss = MySQLdb_finder_2_rows("Fooian_fooers")
    logger.info(f"sql py test:: Make_sql_2_rows length:{len(ss)}")
