#!/usr/bin/python3
""" """
import logging
import re

from apis import mdwiki_api
from copy_to_en.bots import text_changes  # text = text_changes.work(text)
from copy_to_en.bots.ref import fix_ref  # text = fix_ref(first, alltext)
from mdapi_sql import sql_for_mdwiki

logger = logging.getLogger(__name__)


text_cache = {}
revid_cache = {}
un_wb_tag_cache = {}

mdwiki_cats = sql_for_mdwiki.get_db_categories()

full_translate = sql_for_mdwiki.select_md_sql(
    "select DISTINCT tt_title from translate_type where tt_full = 1;", return_dict=True
)

full_translate = [ta["tt_title"] for ta in full_translate]


def get_cats(alltext):
    # ---
    cats = []
    # ---
    for category in mdwiki_cats:
        # ---
        mat = re.search(rf"\[\[Category:{category}(\]\]|\|)", alltext, re.IGNORECASE)
        # ---
        if mat:
            cats.append(category)
    # ---
    cats = list(set(cats))
    # ---
    # if len(cats) > 1 and "RTT" in cats: cats.remove("RTT")
    # ---
    cats_text = "\n".join([f"[[Category:{x}]]" for x in cats])
    # ---
    return cats_text


def get_text_revid(x):
    alltext, revid = mdwiki_api.GetPageText(x, get_revid=True)
    # ---
    text_cache[x] = alltext
    revid_cache[x] = revid
    # ---
    return alltext, revid


def get_un_wb_tag(alltext, x):
    # search for text like {{#unlinkedwikibase:id=Q423364}}
    pattern = r"\{\{#unlinkedwikibase:id=Q[0-9]+\}\}"
    # ---
    match = re.search(pattern, alltext)
    # ---
    unlinkedwikibase = match.group(0) if match else ""
    # ---
    # matches = re.findall(pattern, alltext)
    # for m in matches:
    #     unlinkedwikibase = m
    #     break
    # ---
    un_wb_tag_cache[x] = unlinkedwikibase
    # ---
    return unlinkedwikibase


def get_text(x):
    """Retrieve and process text from a specified page.
    This function fetches the text content of a page using the
    `mdwiki_api.GetPageText` method. It processes the retrieved text to
    extract and format specific information, including handling unlinked
    Wikibase IDs and adjusting the infobox formatting. The function also
    ensures that references are properly formatted and included in the
    output.
    Args:
        x (str): The identifier of the page from which to retrieve text.
    Returns:
        tuple: A tuple containing the processed text and the revision ID
        of the page.
    """
    alltext, revid = get_text_revid(x)
    # ---
    revid_temp = f"{{{{mdwiki revid|{revid}}}}}"
    # ---
    if not alltext:
        logger.info("no text: " + x)
        return "", ""
    # ---
    if x.strip().lower().startswith("video:") or x.strip() in full_translate:
        newtext = text_changes.do_text_fixes(alltext)
        newtext = f"{revid_temp}\n{newtext}"
        return newtext, revid
    # ---
    page_cats = get_cats(alltext)
    # ---
    unlinkedwikibase = get_un_wb_tag(alltext, x)
    # ---
    first = alltext.split("==")[0].strip()
    # ---
    first = first + "\n\n==References==\n<references />"
    newtext = first
    # ---
    newtext = fix_ref(first, alltext)
    # ---
    newtext = text_changes.do_text_fixes(newtext)
    # ---
    # newtext += "\n[[Category:Mdwiki Translation Dashboard articles]]"
    # ---
    newtext = f"{unlinkedwikibase}\n{revid_temp}\n{newtext}\n{page_cats}"
    # ---
    return newtext, revid
