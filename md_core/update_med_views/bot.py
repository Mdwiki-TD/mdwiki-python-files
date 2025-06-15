#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/bot local ask

"""
import tqdm
import sys
import datetime
# ---
from newapi.mdwiki_page import md_MainPage
from update_med_views.views import load_one_lang_views
from update_med_views.helps import count_all_langs, one_lang_titles
from update_med_views.titles import load_one_lang_titles


def get_one_lang_views(langcode, year):
    # ---
    titles = load_one_lang_titles(langcode)
    # ---
    if not titles:
        titles = one_lang_titles(langcode)
    # ---
    views_t = load_one_lang_views(langcode, titles, year)
    # ---
    return views_t


def get_all_views(languages, year):
    # ---
    views = {}
    # ---
    for lang, _ in languages.items():
        views[lang] = get_one_lang_views(lang, year)
    # ---
    return views


def make_text(languages, views):

    # count all languages values
    total_views = sum(views.values())
    # ---
    text = '{{WPM:WikiProject Medicine/Total medical views by language}}\n'
    # ---
    text += f'Total views for medical content = {total_views:,}\n\n'
    # ---
    text += '''{| class="wikitable sortable"\n!Rank\n!Lang\n!# of articles\n!Total views\n!Ave. views\n|----'''
    # ---
    # sort languages by count
    languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=True)}
    # ---
    for n, (lang, articles) in enumerate(languages.items(), start=1):
        # ---
        lang_views = views[lang]
        # ---
        print(lang_views, articles)
        # ---
        Average_views = lang_views // articles if articles and lang_views else 0
        # ---
        text += f'\n|{n}\n|{lang}\n|{articles:,} \n|{lang_views:,}\n|{Average_views:,}\n|-'
    # ---
    text += '\n|}'
    # ---
    return text


def make_views(languages, year, limit):
    # ---
    views = {}
    # ---
    n = 0
    # ---
    for lang, _ in tqdm.tqdm(languages.items()):
        n += 1
        # ---
        if limit > 0 and n > limit:
            print(f"limit {limit} reached, break")
            break
        # ---
        views[lang] = get_one_lang_views(lang, year)
    # ---
    return views


def start(year):
    # ---
    limit = 0
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg.lower() in ['limit', '-limit'] and value.isdigit():
            limit = int(value)
    # ---
    title = f"WikiProjectMed:WikiProject Medicine/Stats/Total pageviews by language {year}"
    # ---
    languages = count_all_langs()
    # ---
    # sort languages ASC
    languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=True)}
    # ---
    views = make_views(languages, year, limit)
    # ---
    text = make_text(languages, views)
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    # ---
    page.save(newtext=text, summary='update', nocreate=0, minor='')


if __name__ == "__main__":
    year = datetime.datetime.now().year
    start("2024")
