"""

يعمل هذا البوت على إضافة PD-medical
إلى الصور الموجودة في تصنيفات الكتاب الأمريكيين

python3 core8/pwb.py mass/radio/authors_list/usa_images test

tfj run usaimages1 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/usa_images"

"""

import sys

from newapi import printe
from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage

from mass.radio.authors_list.usa import get_usa_auths

# from mass.radio.lists.cases_to_cats import cases_cats# cases_cats()
# from mass.radio.authors_list import auths_cats

# from mass.radio.lists.PD_medical import PD_medical_pages_def
# PD_medical_pages = PD_medical_pages_def()
# id2cat = cases_cats()
# auth_cats = auths_cats.get_auth_cats(id2cat, auth)
# usa_auths = get_usa_auths()

PD_medical_pages = []


def add_pd_to_images(not_in_pd: list) -> None:
    printe.output(f"\t\tadd_pd_to_images: {len(not_in_pd)}")
    # ---
    pd_temp = "{{PD-medical}}"
    # ---
    for image in not_in_pd:
        # ---
        if not image.startswith("File:"):
            continue
        # ---
        page = ncc_MainPage(image, "www", family="nccommons")
        text = page.get_text()
        # ---
        new_text = text
        # ---
        if pd_temp in text:
            printe.output(f"\t\t\tno need to add {pd_temp} to {image}")
            continue
        # ---
        add_after = ["{{CC-BY-NC-SA-3.0}}", "== {{int:license}} =="]
        # ---
        for add in add_after:
            if add in text:
                new_text = new_text.replace(add, f"{add}\n{pd_temp}")
                break
        # ---
        if new_text == text:
            new_text = new_text.replace("[[Category:",
                                        f"{pd_temp}\n[[Category:", 1)
        # ---
        if new_text == text:
            new_text = new_text + f"\n{pd_temp}"
        # ---
        if new_text != text:
            page.save(newtext=new_text, summary=f"Bot: add {pd_temp}")


def get_cats_images(cats: list) -> list:
    printe.output(f"\tget_cats_images: {len(cats)}")
    # ---
    result = {}
    # ---
    for cat in cats:
        cat_members = CatDepth(
            cat,
            sitecode="www",
            family="nccommons",
            depth=1,
            onlyns=6,
            tempyes=["Template:PD-medical"],
        )
        # ---
        result.update(cat_members)
    # ---
    printe.output(f"\t{len(result)=}")
    # ---
    return result


def one_auth_wrk(auth: str, auth_cats: list) -> None:
    """
    work on one author cats
    """
    printe.output(f"\tProcessing author {auth} with categories {auth_cats}")

    all_auth_images = get_cats_images(auth_cats)
    printe.output(f"\tall_auth_images: {len(all_auth_images)}")
    # print(all_auth_images)

    # images has "Template:PD-medical" in thir "templates"
    in_pd = {
        image: va
        for image, va in all_auth_images.items()
        if "Template:PD-medical" in va["templates"]
    }
    printe.output(f"\tin_pd: {len(in_pd)}")

    # images not in in_pd
    not_in_pd = set(all_auth_images) - set(in_pd)
    printe.output(f"\tnot_in_pd: {len(not_in_pd)}")

    # add {{PD-medical}} to all images
    add_pd_to_images(not_in_pd)


def start(usa_auths: list = []) -> None:
    # id2cat = cases_cats()
    # ---
    if not usa_auths:
        usa_auths = get_usa_auths()
    # ---
    for n, auth in enumerate(usa_auths, 1):
        # auth_cats = auths_cats.get_auth_cats(id2cat, auth)
        auth_cats = [f"Category:Radiopaedia cases by {auth}"]
        # ---
        printe.output(
            f"<<green>>usa_images: {n}/{len(usa_auths)}: {auth=}, length: {len(auth_cats)}"
        )
        one_auth_wrk(auth, auth_cats)


def test() -> None:
    usa_auths = ["Jonathan Minkin"]
    start(usa_auths)


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
        exit()
    # ---
    start()
