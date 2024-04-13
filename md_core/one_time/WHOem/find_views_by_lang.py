'''

python3 core8/pwb.py WHOem/find_views_by_lang

'''
import sys
import json
import os
from pathlib import Path
import codecs

# ---
from mdpy import printe
from mdpy.bots import wiki_api

# ---
TEST = False
# ---
Dir = Path(__file__).parent
# ---
file = f'{Dir}/lists/views.json'
# ---
if not os.path.exists(file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump({}, f)
# ---
with codecs.open(file, 'r', encoding='utf-8') as f:
    ViewsData = json.load(f)
# ---
N_g = 0


def dump_data(file, data):
    printe.output(f'<<green>> dump_data() file:{file}.')
    printe.output(f'<<yellow>> dump_data {len(data)} views')
    try:
        with codecs.open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except KeyboardInterrupt:
        printe.output('<<red>> keyboard interrupt sys.exit()')
        # ---
        with codecs.open(f'{file}_1', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        # ---
        sys.exit()
    except Exception as e:
        printe.output(f'<<red>> dump Error: {e}')


def get_v(lang, links, lang_links_mdtitle_s):
    # ---
    global ViewsData, N_g
    # ---
    len_p = len(links)
    # -- -
    if 'new' in sys.argv:
        links = {x: t for x, t in links.items() if ViewsData[t].get(lang, {}).get('views', 0) == 0}
        de = len_p - len(links)
        printe.output(f'de: {de}')
    # ---
    # split links to groups by 10 titles
    for i in range(0, len(links), 10):
        group = dict(list(links.items())[i: i + 10])
        # ---
        views_tab = wiki_api.get_views_with_rest_v1(lang, group.keys())
        # ---
        for title, views in views_tab.items():
            # ---
            # _views_ = {"all": 14351,"2021": {"all": 907,"202108": 186},"2022": {"all": 5750,"202201": 158}}
            # ---
            mdtitle = lang_links_mdtitle_s.get(lang, {}).get(title, None)
            if mdtitle is None:
                continue
            # ---
            views = views['all']
            # ---
            viws_in = ViewsData[mdtitle].get(lang, {}).get('views', 0)
            # ---
            printe.output(f't: {title} - {lang} - views: {views}')
            # ---
            # ViewsData.setdefault(mdtitle, {})[lang] = ViewsData[mdtitle].setdefault(lang, {})
            # ---
            # ViewsData.setdefault(mdtitle, {})
            if mdtitle not in ViewsData.keys():
                ViewsData[mdtitle] = {}
            # ---
            # ViewsData[mdtitle].setdefault(lang, {})
            if lang not in ViewsData[mdtitle].keys():
                ViewsData[mdtitle][lang] = {}
            # ---
            if viws_in > 0 and views == 0:
                continue
            # ---
            ViewsData[mdtitle][lang] = {"title": title, "views": views}
            # ---
            N_g += 1
            # ---
            if N_g % 100 == 0:
                dump_data(file, ViewsData)


def get_lang_links_mdtitles(lang_links):
    # ---
    lang_links_mdtitles = {lang: {} for mdtitle, tab in lang_links.items() for lang in tab['langs'].keys()}
    # ---
    for lang in lang_links_mdtitles.keys():
        lang_links_mdtitles[lang] = {tab['langs'][lang]: md for md, tab in lang_links.items() if lang in tab['langs']}
    # ---
    with codecs.open(f'{Dir}/lists/lang_links_mdtitles.json', 'w', encoding='utf-8') as f:
        json.dump(lang_links_mdtitles, f, ensure_ascii=False, indent=2)
    # ---
    # sort lang_links_mdtitles by lenth
    lang_links_mdtitles = dict(sorted(lang_links_mdtitles.items(), key=lambda x: len(x[1]), reverse=True))
    # ---
    # print first 10 of lang_links_mdtitles
    to_p = dict(list(lang_links_mdtitles.items())[0:10])
    # ---
    for x, z in to_p.items():
        print(x, len(z))
    # ---
    return lang_links_mdtitles


def start():
    # ---
    with codecs.open(f'{Dir}/lists/lang_links.json', 'r', encoding='utf-8') as f:
        lang_links = json.load(f)  # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
    # ---
    lang_links_mdtitles = get_lang_links_mdtitles(lang_links)
    # ---
    # len of tab in lang_links
    all_lenth = sum(len(tab.keys()) for tab in lang_links_mdtitles.values())
    # ---
    to_work = lang_links_mdtitles
    # ---
    n = 0
    # ---
    for lang, tab in to_work.items():
        # ---
        n += 1
        # ---
        ViewsData.update({x: {} for x in tab.values() if x not in ViewsData})
        # ---
        printe.output(f'<<blue>> p:{n}/{all_lenth} lang: {lang}, titles: {len(tab)}')
        # ---
        get_v(lang, tab, lang_links_mdtitles)
        # ---
    # ---
    dump_data(file, ViewsData)


if __name__ == '__main__':
    start()
