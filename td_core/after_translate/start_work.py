#!/usr/bin/python3
"""

from after_translate import start_work
# start_work.start(result, lange, tgd, tgd_by_md, tit_user_lang)
# start_work.work_not_pages()

"""

import logging
import re
import sys

from after_translate.bots.fixcat import cat_for_pages
from after_translate.bots.users_pages import not_pages
from mdpy.bots import py_tools

logger = logging.getLogger(__name__)

# ---
titles_not_0 = []
# ---
Skip_titles = {
    "Mr. Ibrahem": {
        "targets": [
            "جامعة نورث كارولاينا",
            "جامعة ولاية كارولينا الشمالية إيه آند تي",
            "نيشان راجاميترابورن",
        ],
        "mdtitles": [],
    },
    "Avicenno": {
        "targets": ["ألم فرجي", "لقاح المكورة السحائية", "استئصال اللوزتين"],
        "mdtitles": [],
    },
    "Subas Chandra Rout": {
        "targets": [],
        "mdtitles": [
            "Wilms' tumor",
            "Sheehan's syndrome",
            "Membranous nephropathy",
        ],
    },
}
# ---
Skip_titles_global = [
    "جامعة نورث كارولاينا",
    "جامعة ولاية كارولينا الشمالية إيه آند تي",
    "نيشان راجاميترابورن",
    "موميتازون",
]


def start(result, lange, tgd, tgd_by_md, tit_user_lang):
    printe.output(f'sql.py len(result) = "{len( result )}"')
    # ---
    tab_lang = {}
    # ---
    to_add = 0
    done = 0
    # ---
    for lis in result:
        # ---
        done += 1
        # ---
        target = lis["title"]
        co_text = lis["comment_text"]
        user = lis["actor_name"]
        pupdate = lis["rev_timestamp"]
        ns = str(lis["page_namespace"])
        # ---
        pupdate = pupdate[:8]
        pupdate = re.sub(r"^(\d\d\d\d)(\d\d)(\d\d)$", r"\g<1>-\g<2>-\g<3>", pupdate)
        # ---
        md_title = co_text.replace("_", " ").strip()
        md_title = re.sub("/full$", "", co_text)
        # ---
        target = target.replace("_", " ")
        # ---
        target = f"user:{target}" if ns == "2" else target
        # ---
        user = user.replace("_", " ")
        # ---
        # tgd_by_md
        target_in = tgd_by_md.get(md_title, "")
        # ---
        line_p = "<<yellow>>{}:<<default>>{},\t"
        # ---
        laox = line_p.format("md_title", md_title)
        laox += line_p.format("user", user)
        laox += line_p.format("ns", ns)
        laox += line_p.format("target", f"[[{lange}:{target.ljust(20)}]]")
        laox += line_p.format("pupdate", pupdate)
        # ---
        if ns != "0" and target_in != target:
            # laox += f", <<purple>>[[{target_in=}]]"
            laox += line_p.format("target_in", target_in)
        # ---
        if "print" in sys.argv:
            printe.output(laox)
        # ---
        if target in Skip_titles_global:
            continue
        if target in Skip_titles.get(user, {}).get("targets", []):
            continue
        # ---
        if md_title in Skip_titles.get(user, {}).get("mdtitles", []):
            continue
        # ---
        Taba2 = {
            "mdtitle": md_title,
            "target": target,
            "user": user,
            "lang": lange,
            "pupdate": pupdate,
            "namespace": ns,
        }
        # ---
        target2 = py_tools.ec_de_code(target, "encode")
        # ---
        tul = md_title + user + lange
        tul_target = tit_user_lang.get(tul, "")
        # ---
        cattest = cat_for_pages.get(md_title, "")
        # ---
        # if ns != "0":
        if target_in != "" and target_in != target:
            if "ns" in sys.argv and tul_target == "" and cattest:
                printe.output(laox)
            continue
        # ---
        not_puplished = target2 not in tgd and target not in tgd
        # ---
        # للتأكد من الصفحات غير المنشورة
        if not_puplished and target_in == "":
            # ---
            if not tul_target:
                printe.output(laox)
                to_add += 1
                tab_lang[md_title] = Taba2
                # ---
                if ns != "0":
                    titles_not_0.append(Taba2)

            elif tul_target == target:
                printe.output(f"target already in, {target}")

            else:
                printe.output(f"puplished target: {tul_target} != target to add: {target}")
    # ---
    printe.output(f"lang: {lange} done: {done}, to_add: {to_add}")
    # ---
    return tab_lang


def work_not_pages():
    not_pages(titles_not_0)
