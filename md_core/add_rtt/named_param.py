#!/usr/bin/python3
"""

python3 core8/pwb.py add_rtt/named_param

"""
# ---
import wikitextparser as wtp

from newapi import printe
from newapi.mdwiki_page import NEW_API, md_MainPage

api_new = NEW_API("www", family="mdwiki")
# api_new.Login_to_wiki()

target_templates = [
    "infobox medical condition",
    "infobox medical condition (new)",
]


def gt_arg(temp, name):
    if temp.has_arg(name):
        va = temp.get_arg(name)
        if va and va.value and va.value.strip():
            return va.value.strip()
    return False


def work_page(title):

    page = md_MainPage(title, "www", family="mdwiki")

    if not page.exists():
        return False

    text = page.get_text()

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
        if name in target_templates:
            # ---
            if temp.has_arg(param):
                value = temp.get_arg(param).value
                printe.output(f"page {title} already had temp {name} with (|{param}={value}). ")
                return False
            # ---
            for x in false_params:
                value = gt_arg(temp, x)
                if value:
                    printe.output(f"page {title} already had temp {name} with (|{x}={value}). ")
                    return False
            # ---
            t_value = ""
            # ---
            if temp.has_arg("eponym"):
                if gt_arg(temp, "eponym"):
                    t_value = gt_arg(temp, "eponym")
                # ---
                temp.del_arg("eponym")
            # ---
            temp.set_arg(param, t_value)
    # ---
    newtext = parsed.string

    save = page.save(newtext=newtext, summary="Added |named after=", nocreate=1, minor="")

    return save


def main():

    temps = "|".join(f"Template:{x}" for x in target_templates)

    temp_pages = api_new.Get_template_pages(temps, namespace=0)

    printe.output(f"len of temp_pages: {len(temp_pages)}")

    for x in temp_pages:
        work_page(x)


if __name__ == "__main__":
    main()
