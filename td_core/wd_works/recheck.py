#!/usr/bin/python3
"""
التحقق من ربط المقالات بالعنصر المناسب في ويكي بيانات

xpython3 core8/pwb.py wd_works/recheck

"""

from pymysql.converters import escape_string
import logging
import sys

from apis import wikidataapi

# ---
from mdapi_sql import sql_for_mdwiki, wiki_sql
from mdpy.bots import en_to_md, py_tools

logger = logging.getLogger(__name__)

targets_done = {}
wd_tt = {}


def dodo_sql():
    # ---
    lang_o = ""
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg in ["lang", "-lang"]:
            lang_o = value
    # ---
    que = """ select title,user,lang,target from pages #where (target = "" OR target IS NULL)"""
    # ---
    if lang_o != "":
        que += f'\n where lang = "{lang_o}"'
    # ---
    que += "\n;"
    # ---
    logger.info(que)
    # ---
    sq = sql_for_mdwiki.select_md_sql(que, return_dict=True)
    # ---
    len_no_target = 0
    len_done_target = 0
    # ---
    for tab in sq:
        title = tab.get("title", "")
        user = tab.get("user", "")
        target = tab.get("target", "")
        # ---
        lang = tab.get("lang", "")
        # ---
        if not lang:
            continue
        # ---
        lang = lang.lower()
        # ---
        if lang_o != "" and lang != lang_o.strip():
            continue
        # ---
        len_done_target += 1
        if lang not in targets_done:
            targets_done[lang] = {}
        target = target.replace("_", " ")
        # targets_done[lang][py_tools.ec_de_code(target , 'encode')] = { "user" : user , "target" : target, "mdtitle" : title }
        targets_done[lang][target] = {"user": user, "target": target, "mdtitle": title}
    # ---
    logger.info(f"<<yellow>> find {len_done_target} with target, and {len_no_target} without ")


def do_it_sql(lange, targets):
    # ---
    titles = list(targets.keys())
    # ---
    for i in range(0, len(titles), 100):
        group = titles[i : i + 100]
        # ---
        ase = [escape_string(t.strip().replace(" ", "_")) for t in group if t.strip() != ""]
        # ---
        if not ase:
            continue
        # ---
        laly = "', '".join(ase)
        # ---
        query = f"""
            select DISTINCT p.page_title, pp.pp_value
            from page p, page_props pp
            where p.page_id = pp.pp_page
            and pp.pp_propname='wikibase_item'
            and p.page_namespace = 0
            and p.page_title in ('{laly}')
            ;"""
        # ---
        result = wiki_sql.Make_sql_many_rows(query, wiki=str(lange))
        # ---
        res_len = len(result)
        # ---
        if res_len == len(group):
            logger.info("<<green>> len(result) == len(group) 100.")
        # ---
        result_n = []
        # ---
        if result:
            logger.info(f'recheck.py len(result) = "{res_len}"')
            # ---
            for liste in result:
                # ---
                target = py_tools.Decode_bytes(liste[0])
                pp_value = py_tools.Decode_bytes(liste[1])
                # ---
                target = target.replace("_", " ")
                result_n.append(target)
                # ---
                md_title = targets.get(target, {}).get("mdtitle", "")
                # ---
                target_tab = {"mdtitle": md_title, "lang": lange, "qid": pp_value}
        # ---
        if res_len < len(group):
            diff = len(group) - res_len
            # logger.info( query )
            itemdiff = [t for t in group if t.strip() != "" and t not in result_n]
            len_missing = len(itemdiff)
            if len_missing > 0:
                logger.info(f"recheck.py {diff} missing from {len(group)}")
                logger.info(f"recheck.py missing:({len_missing}):{','.join(itemdiff)}")


def work_with_2_qids(oldq, new_q):
    # ---
    logger.info("=============================")
    logger.info(f"start:work_with_2_qids: oldq:{oldq}, new_q:{new_q}")
    # ---
    fas = wikidataapi.Get_sitelinks_From_Qid(oldq)
    # {'sitelinks': {'enwiki': 'User:Mr. Ibrahem/Baricitinib', 'orwiki': 'ବାରିସିଟିନିବ'}, 'q': 'Q112331510'}
    # ---
    false_sitelinks = fas.get("sitelinks", {})
    # ---
    len_sites = len(false_sitelinks)
    # ---
    logger.info(f"<<blue>> len_sites {len_sites}")
    # ---
    logger.info(false_sitelinks)
    # ---
    en = false_sitelinks.get("enwiki", "")
    # ---
    if en.startswith("User:Mr. Ibrahem"):
        logger.info(f"<<blue>> remove sitelink {en}")
        remove = wikidataapi.post({"action": "wbsetsitelink", "id": oldq, "linksite": "enwiki"}, token=True)
        if "success" in remove:
            len_sites -= 1
            logger.info("<<green>> **remove sitelink true.")
        else:
            logger.info("<<red>> **remove sitelink false.")
            logger.info(remove)
        # ---
        remove2 = wikidataapi.Labels_API(oldq, "", "en", remove=True)
        # ---
        if remove2:
            len_sites -= 1
            logger.info("<<green>> **remove2 label true.")
        else:
            logger.info("<<red>> **remove2 label false.")
    # ---
    if len_sites in [1, 0]:
        logger.info("<<blue>> merge qids")
        wikidataapi.WD_Merge(oldq, new_q)
    # ---
    logger.info(" work_with_2_qids ends.........")
    logger.info("=============================")


def start():
    # ---
    dodo_sql()
    # ---
    for lange in targets_done:
        # logger.info( ' ================================ ')
        # logger.info( 'mdwiki/mdpy/sql.py: %d Lang : "%s"' % (numb_lang,lange) )
        # ---
        # if "sql" in sys.argv:
        do_it_sql(lange, targets_done[lange])
    # ---
    mdwiki_empty_qids = {}
    qids_to_merge = {}
    empty_qid_target = []
    # ---
    for target, target_tab in wd_tt.items():
        mdtitle = target_tab["mdtitle"]
        lang = target_tab["lang"]
        # ---
        qid_target = target_tab["qid"]
        qid_mdwiki = en_to_md.mdtitle_to_qid.get(mdtitle, "")
        # ---
        tit2 = en_to_md.enwiki_to_mdwiki.get(mdtitle, "")
        qid_2 = en_to_md.mdtitle_to_qid.get(tit2, "")
        # ---
        line22 = f"{lang}:{target}:{qid_target}"
        # ---
        # logger.info( 'recheck: target:%s, lang:%s' % (target,lang) )
        # ---
        if qid_mdwiki == "" and qid_2 == "":
            # logger.info( '<<red>> qid_mdwiki is empty for mdtitle:%s' % mdtitle )
            mdwiki_empty_qids[mdtitle] = (lang, target, qid_target)
            continue
        # ---
        if not qid_target:
            empty_qid_target.append(f"{line22},qid_mdwiki:{qid_mdwiki}")
            # logger.info( '<<red>> qid_target is empty> target:%s' % dsd )
            continue
        # ---
        if qid_mdwiki == "" and qid_2 != "":
            mdtitle = tit2
            qid_mdwiki = qid_2
            logger.info(f"<<yellow>> mdtitle: ({mdtitle}), tit2: ({tit2})")
            logger.info("<<yellow>> qid_mdwiki for mdtitle is empty, but qid_2 for tit2 is not empty")
        # ---
        if qid_target == qid_mdwiki:
            continue
        # ---
        # logger.info( '<<red>> qid_target != qid_mdwiki' )
        # ---
        qids_to_merge[qid_target] = {"wd_qid": qid_mdwiki, "md_title": mdtitle, "lang": lang}
    # ---
    logger.info(f'len(qids_to_merge) = "{len(qids_to_merge)}"')
    # ---
    for oldq, tab in qids_to_merge.items():
        new_q = tab["wd_qid"]
        md_title = tab["md_title"]
        logger.info(f"<<blue>> oldq:{oldq}, new_q:{new_q},md_title:{md_title}")
        # ---
        work_with_2_qids(oldq, new_q)
    # ---
    quary = """
        SELECT ?q ?qlabel
            WHERE {
            ?pid rdfs:label ?qlabel. FILTER((LANG(?qlabel)) = "en").
            FILTER (CONTAINS(?qlabel, "User:Mr. Ibrahem")).
            }
            LIMIT 100
    """
    # newtabs = get_query_result(quary)
    newtabs = wikidataapi.wbsearchentities("User:Mr. Ibrahem", "en")
    # ---
    numb = 0
    # ---
    logger.info("work with newtabs: ")
    logger.info(f'len(newtabs) = "{len(newtabs)}"')
    # ---
    for oldqid, tab in newtabs.items():
        # ---
        en = tab.get("label", "").replace("User:Mr. Ibrahem/", "")
        # ---
        numb += 1
        print(f"------------------\n{numb}/{len(newtabs)}")
        print(f"false qid : {oldqid}")
        print(f"en title: {en}")
        # ---
        # get qid for en page
        qid2 = en_to_md.mdtitle_to_qid.get(en, "")
        if not qid2:
            en2 = en_to_md.enwiki_to_mdwiki.get(en, en)
            qid2 = en_to_md.mdtitle_to_qid.get(en2, "")
        # ---
        print(f"qid2: {qid2}")
        # ---
        if not qid2:
            print("no qid for en page.")
            continue
        # ---
        remove = wikidataapi.Labels_API(oldqid, "", "en", remove=True)
        # ---
        work_with_2_qids(oldqid, qid2)
    # ---
    logger.info("<<blue>> mdwiki_empty_qids:")
    to_add = {}
    # ---
    for mdm in mdwiki_empty_qids:
        lang, target, qid_target = mdwiki_empty_qids[mdm]
        logger.info(f"<<red>> no qid for md_title:{mdm}> {lang}: {target}, qid: {qid_target}")
        to_add[mdm] = qid_target
    # ---
    logger.info("<<blue>> empty_qid_target:")
    for lal in empty_qid_target:
        logger.info(f"<<red>> qid_target is empty> target:{lal}")
    # ---
    if "add" in sys.argv:
        sql_for_mdwiki.add_titles_to_qids(to_add)


if __name__ == "__main__":
    start()
