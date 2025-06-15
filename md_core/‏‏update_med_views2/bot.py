#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/bot -max:50 ask

python3 core8/pwb.py update_med_views/bot -limit:50
python3 core8/pwb.py update_med_views/bot local ask

tfj run umv --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:1000"

tfj run umvsh --image tf-python39 --command "$HOME/pybot/md_core/update_med_views/run.sh"

"""
import json
import sys
from pathlib import Path
# ---
from newapi import printe
from newapi.mdwiki_page import md_MainPage
from apis import views_rest

from mdapi_sql import wiki_sql

t_dump_dir = Path(__file__).parent / "titles"

if not t_dump_dir.exists():
    t_dump_dir.mkdir()


def dump_one(file, data):
    # ---
    if not data:
        return
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
    print("def get_en_articles():")
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    articles = [x['page_title'] for x in result]
    # ---
    return articles


def dump_all(data):
    file = Path(__file__).parent / "languages_counts.json"
    # ---
    # sort data
    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    # ---
    if data and len(data) > 200:
        dump_one(file, data)


def load_all():
    file = Path(__file__).parent / "languages_counts.json"
    # ---
    if file.exists():
        # ---
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    return {}


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
    print("def count_all_langs_sql():")
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    languages = {x['ll_lang']: x['counts'] for x in result}
    # ---
    if "en" not in languages:
        languages["en"] = len(get_en_articles())
    # ---
    dump_all(languages)
    # ---
    return languages


def count_all_langs():
    # ---
    all_infos = load_all()
    # ---
    if not all_infos and ("local" not in sys.argv):
        return count_all_langs_sql()
    # ---
    if all_infos:
        return all_infos
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
    print(f"def one_lang_titles({langcode}):")
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
    print("def langs_titles():")
    # ---
    result = wiki_sql.sql_new(query, 'enwiki')
    # ---
    titles = {}
    # ---
    for x in result:
        titles.setdefault(x['ll_lang'], []).append(x['ll_title'])
    # ---
    titles["en"] = get_en_articles()
    # ---
    dump_all({x: len(y) for x, y in titles.items()})
    # ---
    return titles


def get_view_file(year, lang):
    # ---
    dir_v = Path(__file__).parent / "views" / str(year)
    # ---
    if not dir_v.exists():
        dir_v.mkdir(parents=True)
    # ---
    return dir_v / f"{lang}.json"


def get_one_lang_views_by_titles(langcode, titles, year):
    # ---
    all_data = {}
    # ---
    for i in range(0, len(titles), 50):
        # ---
        group = titles[i:i + 50]
        # ---
        data = views_rest.get_views_with_rest_v1(langcode, group, date_start=f"{year}0101", date_end=f"{year}1231", printurl=False, printstr=False, Type="daily")
        # ---
        all_data.update(data)
    # ---
    return all_data


def load_one_lang_views(langcode, titles, year):
    # ---
    json_file = get_view_file(year, langcode)
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    printe.output(f"<<green>> load_one_lang_views(lang:{langcode}) \t titles: {len(titles):,}")
    # ---
    data = get_one_lang_views_by_titles(langcode, titles, year)
    # ---
    dump_one(json_file, data)
    # ---
    return data


def dump_data(all_data):
    # ---
    for n, (lang, titles) in enumerate(all_data.items(), start=1):
        # ---
        print(f"dump_data(): lang:{n}/{len(all_data)} \t {lang} {len(titles)}")
        # ---
        file = t_dump_dir / f"{lang}.json"
        # ---
        dump_one(file, titles)
    # ---
    print(f"dump_data: all langs: {len(all_data)}")


def load_lang_titles(lang):
    # ---
    json_file = t_dump_dir / f"{lang}.json"
    # ---
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    if "local" in sys.argv:
        return {}
    # ---
    data = one_lang_titles(lang)
    # ---
    return data


def get_one_lang_views(langcode, year, titles):
    # ---
    views_t = load_one_lang_views(langcode, titles, year)
    # ---
    total = 0
    # ---
    for _, tab in views_t.items():
        total += tab.get("all", 0)
    # ---
    return total


def make_text(languages, views):
    # ---
    total_views = sum(views.values())
    total_articles = sum(languages.values())
    # ---
    text = '{{WPM:WikiProject Medicine/Total medical views by language}}\n'
    # ---
    text += f'* Total views for medical content = {total_views:,}\n'
    text += f'* Total articles= {total_articles:,}\n'
    # ---
    text += '\n'
    # ---
    text += '''{| class="wikitable sortable"\n!Rank\n!Lang\n!# of articles\n!Total views\n!Ave. views\n|----'''
    # ---
    # sort languages by count
    languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=True)}
    # ---
    for n, (lang, articles) in enumerate(languages.items(), start=1):
        # ---
        lang_views = views.get(lang, 0)
        # ---
        Average_views = lang_views // articles if articles and lang_views else 0
        # ---
        text += (
            f'\n|{n}'
            f'\n|[//{lang}.wikipedia.org {lang}]'
            f'\n|{articles:,}'
            f'\n|{lang_views:,}'
            f'\n|{Average_views:,}'
            '\n|-'
        )
    # ---
    text += '\n|}'
    # ---
    return text


def make_views(languages, year, limit, maxv):
    # ---
    views = {}
    # ---
    for n, (lang, _) in enumerate(languages.items(), start=1):
        # ---
        if limit > 0 and n > limit:
            printe.output(f"limit {limit} reached, break")
            break
        # ---
        titles = load_lang_titles(lang)
        # ---
        if maxv > 0 and len(titles) > maxv:
            printe.output(f"<<yellow>> {lang}: {len(titles)} titles > max {maxv}, skipping")
            views[lang] = 0
            continue
        # ---
        views[lang] = get_one_lang_views(lang, year, titles)
    # ---
    return views


def start():
    # ---
    limit = 0
    year = 2024
    maxv = 0
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg.lower() in ['limit', '-limit'] and value.isdigit():
            limit = int(value)
        # ---
        if arg.lower() in ['year', '-year'] and value.isdigit():
            year = int(value)
        # ---
        if arg.lower() in ['max', '-max'] and value.isdigit():
            maxv = int(value)
    # ---
    title = f"WikiProjectMed:WikiProject Medicine/Stats/Total pageviews by language {year}"
    # ---
    languages = count_all_langs()
    # ---
    # sort languages ASC
    languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=False)}
    # ---
    views = make_views(languages, year, limit, maxv)
    # ---
    views_not_0 = len([x for x in views.values() if x > 0])
    # ---
    printe.output(f"<<yellow>> Total views not 0: {views_not_0:,}")
    # ---
    newtext = make_text(languages, views)
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    # ---
    text = page.get_text()
    # ---
    if text == newtext:
        printe.output("No change")
        return
    # ---
    printe.output(f"Total views not 0: {views_not_0:,}")
    # ---
    if page.exists():
        page.save(newtext=newtext, summary='update', nocreate=0, minor='')
    else:
        page.Create(newtext, summary='update')


if __name__ == "__main__":
    start()
