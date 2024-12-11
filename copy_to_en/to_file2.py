#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/to_file2


"""
import sys
import random
import json
import requests
from newapi import printe
from pathlib import Path
from multiprocessing import Pool

from apis import cat_cach
from copy_to_en.medwiki import get_text

dir1 = Path(__file__).parent
Dir = "/data/project/mdwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/mdwiki/mdwiki/public_html/mdtexts"

Dir = Path(Dir)


def fix_title(x):
    return x.replace(" ", "_").replace("'", "_").replace(":", "_").replace("/", "_").replace('"', "_")


class WikiProcessor:
    def __init__(self, title):
        self.base_dir = Dir
        self.title = title
        self.sanitized_name = fix_title(self.title)

    def html_to_segments(self, text):
        url = "https://ncc2c.toolforge.org/textp"
        headers = {"Content-Type": "application/json"}
        payload = {"html": text}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            result = response_data.get("result", None)
            return result
        except requests.exceptions.RequestException as e:
            printe.output(f"html_to_segments(): Error occurred: {e}")
            return None

    def convert_wikitext_to_html(self, text):
        end_point = "https://en.wikipedia.org/api/rest_v1/transform/wikitext/to/html/Sandbox"
        params = {"wikitext": text}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(end_point, headers=headers, data=json.dumps(params))
            return response.text
        except requests.exceptions.RequestException as e:
            printe.output(f"convert_wikitext_to_html(): Error occurred: {e}")
            return None

    def save_text(self, text, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            printe.output(f"save_text(): Exception: {e}")

    def get_page_text(self, page_name):
        newtext, revid = get_text(page_name)

        if not newtext:
            return None

        file_path = self.base_dir / f"wikitext/{self.sanitized_name}.txt"
        self.save_text(newtext, file_path)

        printe.output("<<yellow>> get_page_text True.")

        return newtext

    def to_html(self, wikitext):
        html = self.convert_wikitext_to_html(wikitext)

        if not html:
            return None

        file_path = self.base_dir / f"html/{self.sanitized_name}.html"
        self.save_text(html, file_path)

        printe.output("<<yellow>> to_html True.")
        return html

    def to_segments(self, html_text):
        segments = self.html_to_segments(html_text)

        if not segments:
            return None

        file_path = self.base_dir / f"segments/{self.sanitized_name}.html"
        self.save_text(segments, file_path)

        printe.output("<<yellow>> to_segments True.")

        return segments

    def run(self):
        wikitext = self.get_page_text(self.title)

        if not wikitext:
            printe.output("wikitext is empty..")
            return

        html_text = self.to_html(wikitext)

        if html_text:
            segments = self.to_segments(html_text)


def one_page_new(title):
    bot = WikiProcessor(title)
    bot.run()


def get_all():
    file = Dir / "all_pages.json"
    # ----
    if file.exists() and "nodone" not in sys.argv:
        return json.loads(file.read_text())
    # ----
    all_pages = cat_cach.make_cash_to_cats(return_all_pages=True, print_s=False)
    # ---
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pages))
    # ---
    return all_pages


def start(all_pages):
    # ---
    if "slash" in sys.argv:
        all_pages = [x for x in all_pages if x.find("/") != -1]
    # ---
    # sort all_pages randmly
    random.shuffle(all_pages)
    # ---
    if "multi" in sys.argv:
        pool = Pool(processes=2)
        pool.map(one_page_new, all_pages)
        pool.close()
        pool.terminate()
        return
    # ---
    for n, x in enumerate(all_pages):
        print(f"{n}/{len(all_pages)} : {x}")
        # ---
        one_page_new(x)


def get_done(all_pages):
    # ---
    all_pages = [x.replace(" ", "_") for x in all_pages]
    # ---
    dir_to_fetch = Dir / "segments"
    # ---
    files = list(dir_to_fetch.glob("*.html"))
    # ---
    files = [str(x.name).replace(".html", "") for x in files]
    # ---
    not_done = [x for x in all_pages if x not in files]
    # ---
    """
    for x in not_done[:]:
        x2 = fix_title(x)
        # ---
        if x2 in files:
            not_done.remove(x)
    """
    # ---
    return not_done


def main():
    # ---
    all_pages = get_all()
    # ---
    print(f"all_pages: {len(all_pages)}")
    # ---
    if "nodone" not in sys.argv:
        done = get_done(all_pages)
        # ---
        print(f" done: {len(done)}. add 'nodone' to sys.argv to skip find done pages.")
        # ---
        all_pages = [x for x in all_pages if x not in done]
    # ---
    start(all_pages)


if __name__ == "__main__":
    if "test" in sys.argv:
        one_page_new("Menopause")
    else:
        main()
