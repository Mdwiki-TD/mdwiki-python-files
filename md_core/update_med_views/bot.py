#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/bot -limit:50
python3 core8/pwb.py update_med_views/bot local ask

"""
import tqdm
import sys
import datetime
# ---
from newapi.mdwiki_page import md_MainPage
from update_med_views.views import load_one_lang_views
from update_med_views.helps import count_all_langs
from update_med_views.titles import load_lang_titles


def get_one_lang_views(langcode, year):
    # ---
    titles = load_lang_titles(langcode)
    # ---
    views_t = load_one_lang_views(langcode, titles, year)
    # ---
    total = 0
    # ---
    for _, tab in views_t.items():
        total += tab["all"]
    # ---
    return total


def get_all_views(languages, year):
    # ---
    views = {}
    # ---
    for lang, _ in languages.items():
        views[lang] = get_one_lang_views(lang, year)
    # ---
    return views


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


def make_views(languages, year, limit):
    # ---
    views = {}
    # ---
    for n, (lang, _) in enumerate(languages.items(), start=1):
        # ---
        print(f"make_views(): lang:{n}/{len(languages)} \t {lang}")
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
    languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=False)}
    # ---
    views = make_views(languages, year, limit)
    # ---
    newtext = make_text(languages, views)
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    # ---
    text = page.get_text()
    # ---
    if text == newtext:
        print("No change")
        return
    # ---
    if page.exists():
        page.save(newtext=newtext, summary='update', nocreate=0, minor='')
    else:
        page.Create(newtext, summary='update')


if __name__ == "__main__":
    year = datetime.datetime.now().year
    start("2024")
