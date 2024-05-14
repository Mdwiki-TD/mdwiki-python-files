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

with open(main_dir / "jsons/images.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open(main_dir / "jsons/urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

with open(main_dir / "jsons/urls_to_title.json", "r", encoding="utf-8") as f:
    urls_to_title = json.load(f)

for url, tab in urls.items():
    if tab["title"] and not urls_to_title.get(url, ""):
        urls_to_title[url] = tab["title"]

    for x in tab["cases"]:
        if not urls_to_title.get(x["url"], ""):
            urls_to_title[x["url"]] = x["title"]

for url, info_data in data.items():
    if url not in urls_to_title:
        urls_to_title[url] = ""

no_title = [url for url, title in urls_to_title.items() if not title]
if no_title:
    print(f"Number of urls without title: {len(no_title)}")


def start() -> None:
    # open every link in no_title
    # get title from <meta name="Keywords" content="Cataract Formation after Pars Plana Vitrectomy" />
    # save title in urls_to_title
    # write urls_to_title to urls_to_title.json
    no_2 = 0
    for url in tqdm.tqdm(no_title):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        meta = soup.find("meta", attrs={"name": "Keywords"})
        if meta:
            title = meta["content"]
            urls_to_title[url] = title
            continue
        meta2 = soup.find("meta", attrs={"name": "description"})
        if meta2:
            title = meta2["content"]
            urls_to_title[url] = title
            continue

        no_2 += 1

    with open(main_dir / "jsons/urls_to_title.json", "w", encoding="utf-8") as f:
        json.dump(urls_to_title, f, indent=2)

    print(f"Number of urls without title: {no_2} new!! ")


if __name__ == "__main__":
    start()
