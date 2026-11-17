import logging
import re

import wikitextparser as wtp
from md_core_helps.apis import mdwiki_api_call

logger = logging.getLogger(__name__)


def count_text(text: str):

    parsed = wtp.parse(text)

    # remove cat links
    # for link in parsed.wikilinks:   if ":" in link.title:   tem_text = tem_text.replace(str(link), "")
    # parsed = wtp.parse(tem_text)

    plain = parsed.plain_text()

    # remove numbers in string"
    plain = re.sub(r"\d+", "", plain)

    # get counts of words
    length = len(re.findall(r"\w+", plain))
    return length


def count_all(title: str = "", text: str = ""):

    if text == "" and title != "":
        text = mdwiki_api_call.get_page_text(title)

    parsed = wtp.parse(text)

    pageword = count_text(text)

    section = parsed.get_sections(level=0)[0].contents

    leadword = count_text(section)

    return leadword, pageword


if __name__ == "__main__":
    x = "Spondyloperipheral dysplasia"

    leadword, pageword = count_all(title=x)
    logger.info(f"leadword: {leadword}, pageword: {pageword}")

    pageword2 = mdwiki_api_call.wordcount(x)
    logger.info(f"pageword2: {pageword2}")
