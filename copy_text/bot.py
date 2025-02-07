#!/usr/bin/python3
"""

python3 core8/pwb.py copy_text/bot

tfj run tofiles --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_text/bot"

"""
import sys
import random
import json
import requests
from pathlib import Path
from multiprocessing import Pool

from newapi import printe
from apis import cat_cach
from copy_text.text_bot import get_text
from copy_text.html_bot import fix_html

dir1 = Path(__file__).parent
Dir = "/data/project/medwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/medwiki/new/medwiki.toolforge.org_repo/public_html/mdtexts"


Dir = Path(Dir)

done_pages = {1: 0}
len_of_all_pages = {1: 0}


def fix_title(x):
    return x.replace(" ", "_").replace("'", "_").replace(":", "_").replace("/", "_").replace('"', "_")


class WikiProcessor:
    def __init__(self, title):
        self.base_dir = Dir
        self.title = title
        self.sanitized_name = fix_title(self.title)

        done_pages[1] += 1

        printe.output(f"p:{done_pages[1]}/{len_of_all_pages[1]} sanitized_name: {self.sanitized_name}")

    def html_to_segments(self, text):
        url = "https://ncc2c.toolforge.org/textp"
        headers = {"Content-Type": "application/json"}
        payload = {"html": text}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            result = response_data.get("result", None)

            if result and result.find(">Wikimedia Error<") != -1:
                return None

            return result
        except requests.exceptions.RequestException as e:
            printe.output(f"html_to_segments(): Error occurred: {e}")
            return None

    def convert_wikitext_to_html(self, text):
        # end_point = "https://en.wikipedia.org/api/rest_v1/transform/wikitext/to/html/Sandbox"
        end_point = "https://en.wikipedia.org/w/rest.php/v1/transform/wikitext/to/html/Sandbox"
        # end_point = "https://medwiki.toolforge.org/w/rest.php/v1/transform/wikitext/to/html/Sandbox"
        params = {"wikitext": text}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(end_point, headers=headers, data=json.dumps(params))

            html_text = response.text

            if html_text and html_text.find(">Wikimedia Error<") != -1:
                return None

            return html_text
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
        html = fix_html(html)
        file_path = self.base_dir / f"html/{self.sanitized_name}.html"
        self.save_text(html, file_path)

        printe.output(f"<<yellow>> to_html True. {file_path}")
        return html

    def to_segments(self, html_text):
        segments = self.html_to_segments(html_text)

        if not segments:
            return None

        file_path = self.base_dir / f"segments/{self.sanitized_name}.html"
        self.save_text(segments, file_path)

        printe.output(f"<<yellow>> to_segments True. {file_path}")

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
    all_pages = cat_cach.make_cash_to_cats()
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
    len_of_all_pages[1] = len(all_pages)
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
        printe.output(f"{n}/{len(all_pages)} : {x}")
        # ---
        one_page_new(x)


def get_done(all_pages):
    # ---
    all_pages = [x.replace(" ", "_") for x in all_pages]
    # ---
    dir_to_fetch = Dir / "segments"
    # ---
    done = list(dir_to_fetch.glob("*.html"))
    # ---
    done = [str(x.name).replace(".html", "") for x in done]
    # ---
    not_done = [x for x in all_pages if x not in done]
    # ---
    for x in not_done:
        x2 = fix_title(x)
        # ---
        if x2 in done:
            done.append(x)
    # ---
    return done


def main():
    # ---
    all_pages = get_all()
    # ---
    len_old = len(all_pages)
    # ---
    printe.output(f"all_pages: {len(all_pages)}")
    # ---
    if "nodone" not in sys.argv:
        done = get_done(all_pages)
        # ---
        printe.output(f"<<yellow>> done: {len(done)}. add 'nodone' to sys.argv to skip find done pages.")
        # ---
        all_pages = [x for x in all_pages if fix_title(x) not in done]
    # ---
    printe.output(f"<<green>> all_pages: {len(all_pages)}, len_old: {len_old}")
    # ---
    start(all_pages)


if __name__ == "__main__":
    if "test" in sys.argv:
        one_page_new("Gout")
        one_page_new("Sofosbuvir/daclatasvir")
        one_page_new("Lamivudine/tenofovir")
        one_page_new("WHO AWaRe")
    else:
        main()
