#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/bot -year:2024 ask

python3 core8/pwb.py update_med_views/bot -max:50 ask

python3 core8/pwb.py update_med_views/bot -limit:50
python3 core8/pwb.py update_med_views/bot local ask

tfj run umv --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:1000"

tfj run umvsh --image tf-python39 --command "$HOME/pybot/md_core/update_med_views/run.sh"

"""
import sys
# ---
from newapi import printe
from newapi.mdwiki_page import md_MainPage
from update_med_views.views import load_one_lang_views
from update_med_views.helps import count_all_langs
from update_med_views.titles import load_lang_titles


def get_one_lang_views(langcode, titles, year, maxv=0):
    # ---
    views_t = load_one_lang_views(langcode, titles, year, maxv=maxv)
    # ---
    # print(views_t)
    # ---
    total = 0
    # ---
    for _, views in views_t.items():
        if isinstance(views, dict):
            views = views.get("all", 0)
        # ---
        total += views
    # ---
    if total == 0:
        printe.output(f"<<yellow>> No views for {langcode}")
        # printe.output("views_t" + str(views_t))
        # printe.output("titles" + str(titles))
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
        views[lang] = get_one_lang_views(lang, titles, year, maxv=maxv)
    # ---
    return views


def start(year, limit, maxv):
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


def parse_args():
    year = 2024
    limit = 0
    maxv = 0
    for arg in sys.argv:
        key, _, val = arg.partition(':')
        if key in ['limit', '-limit'] and val.isdigit():
            limit = int(val)
        elif key in ['year', '-year'] and val.isdigit():
            year = int(val)
        elif key in ['max', '-max'] and val.isdigit():
            maxv = int(val)
    return year, limit, maxv


if __name__ == "__main__":
    year, limit, maxv = parse_args()
    start(year, limit, maxv)
