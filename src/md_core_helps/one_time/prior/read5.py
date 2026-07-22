"""
write code to read page in en.wikipedia.org using API, then create list with All links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3 core8/pwb.py prior/read5 dontsave
python3 core8/pwb.py prior/read5 logall split
python3 core8/pwb.py prior/read5 dontsave logall

"""

import json
import logging
import os
import sys

# ---
from pathlib import Path

import wikitextparser

from md_core_helps.one_time.prior import text_bot
from mdwiki_api.mdwiki_page import md_MainPage

logger = logging.getLogger(__name__)

# ---

Dir = str(Path(__file__).parents[0])
# logger.info(f'Dir : {Dir}')
# ---
project_json = f"{Dir}/json"
project_js_new = f"{Dir}/json_langs/"
project_js_newen = f"{Dir}/json_en/"
# ---
"""
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
# ---
text        = page.get_text()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
"""
# ---
replaces = {
    "Syncope": "Syncope (medicine)",
}


def get_all_json():
    All = {}
    allen = {}
    # ---
    # get All json file inside dir project_js_new
    for filename in os.listdir(project_js_new):
        if filename.endswith(".json"):
            filename2 = os.path.join(project_js_new, filename)
            # ---
            logger.info(f"filename: {filename2}..")
            # ---
            data = json.load(open(filename2))
            All = {**All, **data}
    # ---
    for filename in os.listdir(project_js_newen):
        if filename.endswith(".json"):
            filename2 = os.path.join(project_js_newen, filename)
            # ---
            logger.info(f"filename: {filename2}..")
            # ---
            data = json.load(open(filename2))
            # ---
            allen = {**allen, **data}
    # ---
    for a, tab in allen.items():
        if a in All:
            All[a]["extlinks"] = tab["extlinks"]
            All[a]["refsname"] = tab["refsname"]
            All[a]["lead"] = tab["lead"]
            All[a]["old"] = tab.get("old", {})
    # ---
    logger.info(f"new All len:{len(All)}")
    # ---
    return All


class WorkAll:
    def __init__(self) -> None:
        self.title = "WikiProjectMed:List/Prior"
        # ---
        self.All = get_all_json()
        # ---
        self.page = md_MainPage(self.title, "www", family="mdwiki")
        self.text = self.page.get_text()
        # ---
        self.parser = wikitextparser.parse(self.text)
        # ---
        logger.info(f"all_wikilinks: {len(self.parser.wikilinks)}")
        # ---
        self.sections = self.parser.get_sections(include_subsections=False)
        # ---
        self.all_sections = {}

    def get_sectios_links(self) -> None:
        for s in self.sections:
            # ---
            title = s.title
            contents = s.contents
            # ---
            if not contents or title is None:
                continue
            # ---
            # parser2 = wikitextparser.parse(c)
            # wikilinks = parser2.wikilinks
            wikilinks = s.wikilinks
            # ---
            wikilinks = [str(x.title) for x in wikilinks]
            # ---
            wikilinks = [replaces.get(x, x) for x in wikilinks]
            # ---
            if len(wikilinks) == 0:
                continue
            # ---
            title = title.replace("/", "-")
            # ---
            _all_ = {a: self.All[a] for a in wikilinks if a in self.All}
            # ---
            if len(_all_) < 150 or "split" not in sys.argv:
                self.all_sections[title] = _all_
                continue
            # ---
            numb = 150
            # ---
            if title == "Other drugs - procedures":
                numb = 103
            # ---
            elif len(_all_) < 300:
                numb = 150
            elif len(_all_) > 400:
                numb = 120
            # ---
            n = 1
            # ---
            for i in range(0, len(_all_), numb):
                # ---
                las = dict(list(_all_.items())[i : i + numb])
                # ---
                ta = f"{title}_{n}"
                # ---
                self.all_sections[ta] = las
                # ---
                n += 1

    def run(self) -> None:
        # ---
        self.get_sectios_links()
        # ---
        for t, _all_ in self.all_sections.items():
            lrnn = len(_all_.keys())
            # ---
            logger.info(f"<<yellow>> section:({t}), \t\twikilinks: {lrnn}")
            # ---
            ttt = f"User:Mr. Ibrahem/prior/{t}"
            # ---
            filetitle = f"{Dir}/log/{t}.txt"
            # ---
            text = text_bot.make_text(_all_, ttt=t)
            # ---
            if "dontsave" not in sys.argv:
                open(filetitle, "w", encoding="utf-8").write(text)
                # ---
                page_x = md_MainPage(ttt, "www", family="mdwiki")
                # ---
                exists = page_x.exists()
                if not exists:
                    page_x.create(text=text, summary="update")
                # ---
                else:
                    page_x_text = page_x.get_text()
                    # ---
                    page_x.save(newtext=text, summary="update", nocreate=0)


def work_all() -> None:
    # ---
    bot = WorkAll()
    bot.run()
    # ---
    page_x = md_MainPage("User:Mr. Ibrahem/prior", "www", family="mdwiki")
    # ---
    if "dontsave" not in sys.argv:
        t_sec = text_bot.get_t_sections()
        # ---
        page_x.save(newtext=t_sec, summary="update", nocreate=0)
    # ---
    if "logall" in sys.argv:
        text_bot.log_all_pages_states()
    else:
        logger.info('<<yellow>> add "logall" to args to log All pages links green/red..')


if __name__ == "__main__":
    work_all()
