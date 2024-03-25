#!/usr/bin/python3
"""

نسخ التحويلات من الإنجليزية إلى mdwiki

"""

#
# (C) Ibrahem Qasim, 2022
#
#
# ---
# ---

# import datetime
# import dateutil.parser
# import time
# from datetime import datetime, date
import sys

from mdpy import printe

# ---
from mdpy.bots import mdwiki_api

# ---
offset = {1: 0}
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(":")
    # ---
    if arg.lower() in ["offset", "-offset"] and value.isdigit():
        offset[1] = int(value)
# ---
from_to = {}


def fix_dup(From, To):
    """Treat one double redirect."""
    # ---
    targetPage = To
    if To in from_to:
        To = from_to[To]
    # ---
    newtext = f"#REDIRECT [[{To}]]"
    # ---
    oldtext = mdwiki_api.GetPageText(From)
    sus = f"fix duplicate redirect to [[{To}]]"
    mdwiki_api.page_put(
        oldtext=oldtext,
        newtext=newtext,
        summary=sus,
        title=From,
        returntrue=False,
        diff=True,
    )


def main():
    printe.output("*<<lightred>> > main:")
    # ---
    # python3 dup.py -page:Allopurinol
    # python3 dup.py -page:Activated_charcoal_\(medication\)
    # python3 dup.py -newpages:10
    # python dup.py -newpages:1000
    # python dup.py -newpages:20000
    # ---
    fop = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "generator": "querypage",
        "redirects": 1,
        "utf8": 1,
        "gqppage": "DoubleRedirects",
        "gqplimit": "max",
    }
    # ---
    lista = mdwiki_api.post_s(fop)
    # ---
    redirects = lista.get("query", {}).get("redirects", [])
    # ---
    for gg in redirects:
        From = gg["from"]
        To = gg["to"]
        from_to[From] = To
    for nu, title in enumerate(redirects, start=1):
        From = title["from"]
        printe.output('-------------------------------------------\n*<<lightyellow>> >%d/%d From:"%s".' % (nu, len(redirects), From))
        To = title["to"]
        if To in from_to:
            fix_dup(From, To)
    # ---


if __name__ == "__main__":
    main()
