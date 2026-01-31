#!/usr/bin/python3
"""

python3 core8/pwb.py copy_text/html_bot

"""
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def fix_html(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find all anchor elements
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        # Check if 'action=edit' exists in href
        if "action=edit" in href:
            old_link = str(link)
            # Remove '?action=edit' and everything after it
            new_href = href.split("?action=edit")[0]
            link["href"] = new_href

            # Remove unwanted attributes
            for attr in ["typeof", "data-mw-i18n", "class"]:
                if attr in link.attrs:
                    del link[attr]

            # Set new class to 'cx-link'
            link["class"] = "cx-link"
            # new_link = str(link)
            # html = html.replace(old_link, new_link)

    # Return the modified HTML as a string
    return str(soup)


text = """<a rel="mw:WikiLink" href="./Template:Mdwiki_revid?action=edit&amp;redlink=1" title="Template:Mdwiki revid" about="#mwt3" typeof="mw:Transclusion mw:LocalizedAttrs" class="new" data-mw='{"parts":[{"template":{"target":{"wt":"mdwiki revid","href":"./Template:Mdwiki_revid"},"params":{"1":{"wt":"1440189"}},"i":0}}]}' data-mw-i18n='{"title":{"lang":"x-page","key":"red-link-title","params":["Template:Mdwiki revid"]}}' id="mwBA" data-parsoid='{"stx":"simple","a":{"href":"./Template:Mdwiki_revid"},"sa":{"href":":Template:Mdwiki revid"},"pi":[[{"k":"1"}]],"dsr":[33,57,null,null]}'>Template:Mdwiki revid</a>"""

if __name__ == "__main__":
    new_text = fix_html(text)
    printe.showDiff(text, new_text)
