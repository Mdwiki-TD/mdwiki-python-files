"""

python3 core8/pwb.py mass/eyerounds/bots/url_to_title

from mass.eyerounds.bots.url_to_title import urls_to_title

"""
import tqdm
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Specify the root folder
main_dir = Path(__file__).parent.parent

with open(main_dir / 'jsons/images.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(main_dir / 'jsons/urls.json', 'r', encoding='utf-8') as f:
    urls = json.load(f)
with open(main_dir / 'jsons/urls_to_title_new.json', 'r', encoding='utf-8') as f:
    urls_to_title_new = json.load(f)

urls_to_title = urls_to_title_new.copy()

for url, tab in urls.items():

    if tab['title'] and not urls_to_title.get(url, ''):
        urls_to_title[url] = tab['title']

    for x in tab['cases']:
        if not urls_to_title.get(x['url'], ''):
            urls_to_title[x['url']] = x['title']

for url, info_data in tqdm.tqdm(data.copy().items()):
    if url not in urls_to_title:
        urls_to_title[url] = ''

with open(main_dir / 'jsons/urls_to_title.json', 'w', encoding='utf-8') as f:
    json.dump(urls_to_title, f, indent=2)

no_title = [ url for url, title in urls_to_title.items() if not title ]

print(f"Number of urls without title: {len(no_title)}")


def start():
    # open every link in no_title
    # get title from <meta name="Keywords" content="Cataract Formation after Pars Plana Vitrectomy" />
    # save title in urls_to_title
    # write urls_to_title to urls_to_title.json
    for url in tqdm.tqdm(no_title):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta = soup.find('meta', attrs={'name': 'Keywords'})
        if meta:
            title = meta['content']
            urls_to_title_new[url] = title

    with open(main_dir / 'jsons/urls_to_title_new.json', 'w', encoding='utf-8') as f:
        json.dump(urls_to_title_new, f, indent=2)


if __name__ == '__main__':
    start()
