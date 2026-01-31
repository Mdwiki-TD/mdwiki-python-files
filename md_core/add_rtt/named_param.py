#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/named_param

from add_rtt.named_param import add_param_named
# add_param_named(text, title)


tfj run renamep --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py add_rtt/named_param"

"""
from newupdater import expend_infoboxs_and_fix
from newapi.mdwiki_page import NEW_API, md_MainPage
import logging

# ---
import wikitextparser as wtp

logger = logging.getLogger(__name__)

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()


target_infoboxs = [
    "infobox medical condition",
    "infobox medical condition (new)",
]


def gt_arg(temp, name):
    if temp.has_arg(name):
        va = temp.get_arg(name)
        if va and va.value and va.value.strip():
            return va.value.strip()
    return False


def add_param_named(text, title):

    parsed = wtp.parse(text)

    param = "named after"

    false_params1 = [
        "named after",
        "eponym",
    ]
    # ---
    false_params = []

    for temp in parsed.templates:

        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        if name in target_infoboxs:
            # ---
            if temp.has_arg(param):
                value = temp.get_arg(param).value
                printe.output(f"page {title} already had temp {name} with (|{param}={value}). ")
                return text
            # ---
            for x in false_params:
                value = gt_arg(temp, x)
                if value:
                    printe.output(f"page {title} already had temp {name} with (|{x}={value}). ")
                    return text
            # ---
            t_value = ""
            # ---
            if temp.has_arg("eponym"):
                if gt_arg(temp, "eponym"):
                    t_value = gt_arg(temp, "eponym")
                # ---
                temp.del_arg("eponym")
            # ---
            temp.set_arg(f" {param} ", f" {t_value}\n")

    newtext = parsed.string
    newtext = expend_infoboxs_and_fix(newtext)

    return newtext


def work_page(title):

    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False

    text = page.get_text()

    newtext = add_param_named(text, title)

    if newtext != text:
        page.save(newtext=newtext, summary="Add (|named after=) to Infobox medical condition", nocreate=1, minor="")


def main():

    temps = "|".join(f"Template:{x}" for x in target_infoboxs)

    temp_pages = api_new.Get_template_pages(temps, namespace=0)

    printe.output(f"len of temp_pages: {len(temp_pages)}")

    for x in temp_pages:
        work_page(x)


if __name__ == "__main__":
    main()
