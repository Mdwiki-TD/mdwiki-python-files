"""

python3 core8/pwb.py WHOem/lists/lang_links new
#---
"""

import json
import logging
import sys
from pathlib import Path

from mdwiki_api.mdwiki_page import CatDepth
from mdwiki_api.wiki_page import MainPage, change_codes

logger = logging.getLogger(__name__)

# ---

# result_table = CatDepth(title, sitecode="www", family="mdwiki", depth=0, ns="0")
# ---
Dir = Path(__file__).parent
# ---


def get_md_links():
    # ---
    cats = [
        "World Health Organization essential medicines",
        "World Health Organization essential medicines (vaccines)",
        "World Health Organization essential medicines (alternatives)",
        "World Health Organization essential medicines (removed)",
    ]
    # ---
    all_p = []
    # ---
    for cat in cats:
        links = CatDepth(f"Category:{cat}", sitecode="www", family="mdwiki", depth=0, ns="0")
        all_p.extend(links)
        print(f"md_links.py {len(links)} links found")
    # ---
    all_p = list(set(all_p))
    # ---
    with open(f"{Dir}/lists/md_links.json", "w", encoding="utf-8") as f:
        json.dump(all_p, f, ensure_ascii=False, indent=2)
    # ---
    return all_p


def get_lang_links(md_links):
    # ---
    links_not_found = []
    # ---
    with open(f"{Dir}/lists/lang_links.json", "r", encoding="utf-8") as f:
        lang_links = json.load(f)
    # ---
    logger.info(f"list len of it: {len(md_links)}")
    # ---
    n = 0
    # ---
    for x in md_links:
        # ---
        n += 1
        # ---
        if "new" in sys.argv and len(lang_links.get(x, {}).get("langs", {})) > 0:
            continue
        # ---
        pap = f"p {n}/{len(md_links)}: {x}"
        # ---
        logger.info(pap)
        # ---
        title = x
        # ---
        page = MainPage(title, "en")
        # ---
        if not page.exists():
            logger.error(f"<<red>> page: {title} not found in enwiki.")
            links_not_found.append(title)
            return
        # ---
        if title not in lang_links:
            lang_links[title] = {"en": title, "redirect_to": "", "langs": {}}
        # ---
        if page.isRedirect():
            target = page.get_redirect_target()
            if target != "":
                page = MainPage(target, "en")
                lang_links[title]["en"] = target
                lang_links[title]["redirect_to"] = target
        # ---
        langlinks = page.get_langlinks()
        # ---
        langlinks["en"] = title
        # ---
        logger.info(f"<<blue>> en:{title}, \n\tlanglinks: {len(langlinks)}")
        # ---
        for lang, tit in langlinks.items():
            # ---
            lang = change_codes.get(lang) or lang
            # ---
            lang_links[title]["langs"][lang] = tit

    # ---
    with open(f"{Dir}/lists/lang_links.json", "w", encoding="utf-8") as f:
        json.dump(lang_links, f, ensure_ascii=False, indent=2)
    # ---
    logger.error(f"<<red>> len of links_not_found: {len(links_not_found)}:")
    # ---
    with open(f"{Dir}/lists/links_not_found.json", "w", encoding="utf-8") as f:
        json.dump(links_not_found, f, ensure_ascii=False, indent=2)
    # ---
    for title in links_not_found:
        print(f"\t{title}")
    # ---
    return lang_links


def sts():
    md_links = get_md_links()
    # ---
    lang_links = get_lang_links(md_links)


if __name__ == "__main__":
    sts()
