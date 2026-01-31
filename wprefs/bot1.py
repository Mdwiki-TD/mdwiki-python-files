#!/usr/bin/python3
"""

تجميع المراجع في الصفحات

python3 core8/pwb.py wprefs/bot -lang:es ask savetofile
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପାଟେଲୋଫିମୋରାଲ_ଯନ୍ତ୍ରଣା_ସିଣ୍ଡ୍ରୋମ
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପୋଷ୍ଟିରିଅର_ୟୁରେଥ୍ରାଲ_ଭଲଭ ask
python3 core8/pwb.py wprefs/bot -lang:or -page:user:Mr._Ibrahem/sandbox ask

python3 core8/pwb.py wprefs/bot -lang:ro ask

python3 core8/pwb.py wprefs/bot ask

"""
# import os
import random
import sys
from pathlib import Path

if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))

from wprefs.api import GetPageText  # , page_put
from wprefs.files import save_wprefcash, setting
from wprefs.helps import ec_de_code
from wprefs.wpref_text import fix_page

move_dot = {1: False}
expend_infobox = {1: False}


def fix_page_here(text, title, langcode):
    newtext = text
    # ---
    section_0_text = ""
    # ---
    lang_default = setting.get(langcode, {})
    # ---
    dots = move_dot[1]
    if lang_default.get("move_dots", 0) == 1:
        dots = True
    # ---
    expend = expend_infobox[1]
    if lang_default.get("expend", 0) == 1:
        expend = True
    # ---
    adden = False
    if lang_default.get("add_en_lang", 0) == 1:
        adden = True
    # ---
    newtext = fix_page(
        newtext, title, move_dots=dots, infobox=expend, section_0=section_0_text, lang=langcode, add_en_lang=adden
    )
    # ---
    return newtext


def one_page(page, lang):
    """Process a page and update its content based on specified language.

    This function takes a page identifier and a language code, retrieves the
    text associated with the page, and applies various transformations to
    it. If the retrieved text is empty or unchanged after processing,
    appropriate messages are printed. If changes are made, the updated text
    is saved to a file.

    Args:
        page (str): The identifier of the page to be processed.
        lang (str): The language code to be used for retrieving the page text.

    Returns:
        str: An empty string upon completion of the function.
    """

    title = ec_de_code(page, "decode")
    # ---
    text = GetPageText(title, lang=lang, Print=False)
    # ---
    if not text:
        logger.info("notext")
        return ""
    # ---
    newtext = fix_page_here(text, title, lang)
    # ---
    if text == newtext:
        logger.info("no changes")
        return ""
    # ---
    if not newtext:
        logger.info("notext")
        return ""
    # ---
    # if "save" in sys.argv:
    #     a = page_put(text, newtext, "Fix references, Expand infobox mdwiki.toolforge.org.", title, lang)
    #     if a:
    #         logger.info("save ok")
    #         return ""
    # ---
    filee = save_wprefcash(title, newtext)
    logger.info(filee)
    # ---
    return ""


def one_file(file, lang):
    """Process a file and apply transformations based on its content.

    This function reads the content of a specified file, applies a
    transformation using the `fix_page_here` function, and saves the
    modified content if changes are made. It handles file paths and ensures
    that the file is read with UTF-8 encoding. If any errors occur during
    file reading, they are caught and logged, and an empty string is
    returned. The function also generates a random title for the transformed
    content.

    Args:
        file (str): The path to the input file.
        lang (str): The language parameter used for transformation.

    Returns:
        str: An empty string indicating the result of the operation.
    """

    # ---
    text = ""
    # ---
    rand_title = random.randint(1000000, 9999999)
    rand_title = f"t_{rand_title}"
    # ---
    if file.startswith("texts/"):
        file = Dir.parent / "public_html/fixwikirefs" / file
    # ---
    try:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        text = ""
        logger.info(e)
        return ""
    # ---
    if text == "":
        logger.info("notext")
        return ""
    # ---
    newtext = fix_page_here(text, rand_title, lang)
    # ---
    if text == newtext:
        logger.info("no changes")
        return ""
    # ---
    if not newtext:
        logger.info("notext")
        return ""
    # ---
    filee = save_wprefcash(rand_title, newtext)
    # ---
    logger.info(filee)
    # ---
    return ""


def maine():
    """Process command-line arguments and execute corresponding actions.

    This function parses command-line arguments to determine the desired
    actions, such as loading a specific page or file, and setting the
    language for processing. It checks for required parameters and invokes
    the appropriate functions based on the provided arguments. If neither a
    page nor a file is specified, it outputs an error message.

    Returns:
        str: An empty string upon completion of processing.
    """

    # ---
    page = ""
    lange = ""
    file = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        arg = arg[1:] if arg.startswith("-") else arg
        # ---
        if arg == "infobox":
            expend_infobox[1] = True
        if arg == "movedots":
            move_dot[1] = True
        # ---
        if arg == "lang":
            lange = value.strip()
        if arg == "page":
            page = value.replace("_", " ")
        if arg == "file":
            file = value.replace("_", " ")
    # ---
    if page == "" and file == "":
        logger.info("no page or file")
        return ""
    # ---
    if lange == "":
        logger.info("no lang")
        return ""
    # ---
    if file:
        one_file(file, lange)
    else:
        one_page(page, lange)
    # ---
    return ""


if __name__ == "__main__":
    maine()
