"""

python3 core8/pwb.py fix_mass/fix_sets/bots/get_img_info

from fix_mass.fix_sets.bots.get_img_info import one_img_info

"""
import sys
import re
import json
import os
from pathlib import Path

from newapi import printe
from newapi.ncc_page import NEW_API

api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

Dir = Path(__file__).parent.parent

st_dic_infos = Dir / "jsons/studies_files_infos"

def dump_st(data, s_id):
    file = st_dic_infos / f"{s_id}_s_id.json"
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to file: {file}")

def gt_img_info(titles):
    # ---
    titles = [titles] if not isinstance(titles, list) else titles
    # ---
    info = {}
    printe.output(f"one_img_info: {len(titles)=}")
    # ---
    _x = {
        "pages": [
            {
                "pageid": 1382521,
                "ns": 6,
                "title": "File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 4).jpg",
                "extlinks": [
                    {"url": "https://radiopaedia.org/cases/appendicitis-ct-angiogram"},
                    {"url": "https://creativecommons.org/licenses/by-nc-sa/3.0/"},
                    {"url": "http://creativecommons.org/licenses/by-nc-sa/3.0/"},
                    {"url": "https://radiopaedia.org/cases/154713/studies/134732"},
                    {"url": "https://prod-images-static.radiopaedia.org/images/61855973/2bdea73556100c7fb71c76c05394c69df2b00153ab6b00647c53c51ee7c88f3d.jpg"},
                    {"url": "https://radiopaedia.org/users/stefan-tigges?lang=us"},
                ],
            }
        ]
    }
    # ---
    params = {
        "action": "query",
        "titles": "|".join(titles),
        # "prop": "revisions|categories|info|extlinks",
        "prop": "extlinks",
        # "clprop": "sortkey|hidden", # categories
        # "rvprop": "timestamp|content|user|ids", # revisions
        # "cllimit": "max",  # categories
        "ellimit": "max",  # extlinks
        "formatversion": "2",
    }
    # ---
    # work with 40 titles at once
    for i in range(0, len(titles), 40):
        group = titles[i : i + 40]
        params["titles"] = "|".join(group)
        # ---
        # print("|".join(group))
        # ---
        data = api_new.post_params(params)
        # ---
        error = data.get("error", {})
        if error:
            printe.output(json.dumps(error, indent=2))
        # ---
        pages = data.get("query", {}).get("pages", [])
        # ---
        for page in pages:
            extlinks = page.get("extlinks", [])
            title = page.get("title")
            # ---
            info[title] = {"img_url": "", "case_url": "", "study_url": "", "caseId": "", "studyId": ""}
            # ---
            for extlink in extlinks:
                url = extlink.get("url")
                ma = re.match("https://radiopaedia.org/cases/(\d+)/studies/(\d+)", url)
                if url.find("/images/") != -1:
                    info[title]["img_url"] = url

                elif re.match(r"^https://radiopaedia.org/cases/[^\d\/]+$", url):
                    info[title]["case_url"] = url

                elif ma:
                    info[title]["study_url"] = url
                    info[title]["caseId"] = ma.group(1)
                    info[title]["studyId"] = ma.group(2)
    # ---
    # printe.output(json.dumps(pages, indent=2))
    # ---
    return info


def one_img_info(title, study_id):
    # ---
    info = gt_img_info(title)
    # ---
    # printe.output(json.dumps(pages, indent=2))
    # ---
    dump_st(info, study_id)
    # ---
    return info


def test():
    title = ["File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 4).jpg", "File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 2).jpg"]
    info = one_img_info(title)
    # ---
    print(json.dumps(info, indent=2))
    # ---


if __name__ == "__main__":
    test()
