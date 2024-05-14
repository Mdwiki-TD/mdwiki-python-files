# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py mass/eyerounds/all_cats ask

"""
import json
from pathlib import Path
from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage

# Specify the root folder
main_dir = Path(__file__).parent

from mass.eyerounds.bots.url_to_title import urls_to_title
from mass.eyerounds.bots.catbot import category_name


def doo():
    with open(main_dir / "jsons/images.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # names = {}
    cases_done = []
    cases = {}

    for url, info_data in data.items():
        images_info = info_data.get("images", {})
        if not images_info:
            continue
        # if url.lower() in cases_done:   continue
        cases_done.append(url.lower())

        cases[url] = len(images_info.keys())
        # ---
        # for u, name in images_info.items():
        #     if name not in names:
        #         names[name] = 0
        #     names[name] += 1

    done = {}
    text = '{| class="wikitable sortable"\n|-\n' + "! # !! Category !! Image set !! Case number !! Url !! Number of images\n"

    # ---
    def background_color(numb):
        if done.get(numb, 1) > 1:
            # style="background-color:#c79d9d"|
            return ' style="background-color:#c79d9d"| '
        return False

    # ---
    for n, (url, count) in enumerate(cases.items(), start=1):
        x = urls_to_title.get(url)
        # ---
        done.setdefault(x, 0)
        done[x] += 1
        # ---
        done.setdefault(url, 0)
        done[url] += 1
        # ---
        cat, numb = category_name(url)
        # ---
        done.setdefault(numb, 0)
        done[numb] += 1
        # ---
        if not cat:
            cat = f"{x} (EyeRounds)"
        # ---
        done.setdefault(cat, 0)
        done[cat] += 1
        # ---
        bc = background_color(cat) or background_color(numb) or background_color(x) or ""
        # ---
        text += f"|- {bc}\n"
        text += f"! {n}\n"
        text += f"| [[:Category:{cat}]]\n"
        text += f"| [[{cat}|set]]\n"  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f"| {numb}\n"
        text += f"| [{url} ]\n"  # + '|| {{#ifexist:' + x2 + '|1|0}}\n'
        text += f"| {count}\n"

    text += "|}"
    text += "\n[[Category:EyeRounds|*]]"

    page = ncc_MainPage("User:Mr._Ibrahem/EyeRounds", "www", family="nccommons")
    # ---
    old_text = page.get_text()
    # ---
    if old_text != text:
        page.save(newtext=text, summary="update", nocreate=0, minor="")
    else:
        printe.output("<<lightyellow>> No changes")

    # sort names by count
    done = dict(sorted(done.items(), key=lambda x: x[1], reverse=True))

    # print done
    for naa, count in done.items():
        if count > 1:
            print(f"{count}\t\t{naa}")


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    doo()
