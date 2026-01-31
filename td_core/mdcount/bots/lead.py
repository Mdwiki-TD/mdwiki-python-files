# ---
import logging
import re

import wikitextparser as wtp
from apis import mdwiki_api

logger = logging.getLogger(__name__)


# ---


def count_text(text):
    # ---
    text = text.replace("'''", "").replace("''", "")
    # ---
    tem_text = text
    # ---
    parsed = wtp.parse(tem_text)
    # ---
    # remove cat links
    # for link in parsed.wikilinks:   if ":" in link.title:   tem_text = tem_text.replace(str(link), "")
    # parsed = wtp.parse(tem_text)
    # ---
    # remove tables
    # remove template
    # remove html tag include ref tags
    # remove all comments
    # remove all external links
    tem_text = parsed.plain_text()
    parsed = wtp.parse(tem_text)
    # replace all wikilinks to be like  [from|some text ] to from
    # for wikilink in parsed.wikilinks:   tem_text = tem_text.replace(str(wikilink), str(wikilink.title))

    # remove tables like this "{| |}"
    tem_text = re.sub(r"{|\|[.|\w|\W]*?\|}", "", tem_text)

    # remove numbers in string"
    tem_text = re.sub(r"\d+", "", tem_text)

    # get counts of words
    length = len(re.findall(r"\w+", tem_text))
    # ---
    # logger.info(f'count_text: {length}')
    return tem_text, length


def count_all(title="", text=""):
    # ---
    if text == "" and title != "":
        text = mdwiki_api.GetPageText(title)
    # ---
    parsed = wtp.parse(text)
    # ---
    _te_, pageword = count_text(text)
    # ---
    section = parsed.get_sections(level=0)[0].contents
    # ---
    _te_, leadword = count_text(section)
    # ---
    return leadword, pageword


if __name__ == "__main__":
    # ---
    x = "Spondyloperipheral dysplasia"
    # ---
    leadword, pageword = count_all(title=x)
    logger.info(f"leadword: {leadword}, pageword: {pageword}")
    # ---
    pageword2 = mdwiki_api.wordcount(x)
    logger.info(f"pageword2: {pageword2}")
