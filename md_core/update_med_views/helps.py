#!/usr/bin/python3
"""

from update_med_views.helps import count_all_langs, get_en_articles, one_lang_titles, langs_titles

"""
import sys
import datetime
import tqdm
import json
from mdapi_sql import wiki_sql
from update_med_views.titles import t_dump_dir


def get_en_articles():
    # ---
    query = """
        select page_title
            from page, page_assessments, page_assessments_projects
            where pap_project_title = "Medicine"
            and pa_project_id = pap_project_id
            and pa_page_id = page_id
            and page_is_redirect = 0
            and page_namespace = 0
    """
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    articles = [x['page_title'] for x in result]
    # ---
    return articles


def count_all_langs_sql():
    # ---
    query = """
    select ll_lang, count(page_title) as counts
        from page , langlinks , page_assessments , page_assessments_projects
        where pap_project_title = "Medicine"
        and pa_project_id = pap_project_id
        and pa_page_id = page_id
        and page_id = ll_from
        and page_is_redirect = 0
        and page_namespace = 0
        #and ll_lang = 'ar'
        group by ll_lang
        #limit 10
    """
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    languages = {x['ll_lang']: x['counts'] for x in result}
    # ---
    if "en" not in languages:
        languages["en"] = len(get_en_articles())
    # ---
    return languages


def count_all_langs():
    # ---
    if "local" not in sys.argv:
        return count_all_langs_sql()
    # ---
    result = {}
    # ---
    for json_file in t_dump_dir.glob("*.json"):
        lang = json_file.stem
        # ---
        with open(json_file, "r", encoding="utf-8") as f:
            result[lang] = len(json.load(f))
    # ---
    print(f"count_all_langs local: {len(result)}")
    # ---
    return result


def one_lang_titles(langcode):
    # ---
    if langcode == 'en':
        return get_en_articles()
    # ---
    query = """
        select ll_title
            from page, langlinks, page_assessments, page_assessments_projects
            where pap_project_title = "Medicine"
            and pa_project_id = pap_project_id
            and pa_page_id = page_id
            and page_id = ll_from
            and page_is_redirect = 0
            and page_namespace = 0
            and ll_lang = %s
    """
    # ---
    result = wiki_sql.sql_new(query, 'enwiki', values=(langcode,))
    # ---
    titles = [x['ll_title'] for x in result]
    # ---
    return titles


def langs_titles():
    # ---
    query = """
        select ll_lang, ll_title
            from page, langlinks, page_assessments, page_assessments_projects
            where pap_project_title = "Medicine"
            and pa_project_id = pap_project_id
            and pa_page_id = page_id
            and page_id = ll_from
            and page_is_redirect = 0
            and page_namespace = 0
    """
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    titles = {}
    # ---
    for x in result:
        titles.setdefault(x['ll_lang'], []).append(x['ll_title'])
    # ---
    return titles
