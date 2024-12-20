#!/usr/bin/python3
"""
Usage:
from copy_to_en.bots.fix_refs_names import fix_ref_names

python3 core8/pwb.py copy_to_en/bots/fix_refs_names

"""
import wikitextparser as wtp
from newapi import printe


def fix_ref_names(text):
    parsed_page = wtp.parse(text)

    ref_tags = parsed_page.get_tags("ref")

    #  <ref name=Stat2022> to: <ref name="Stat2022">

    for tag in ref_tags:
        if not tag.contents:
            continue
        # ---
        for x in tag.attrs:
            u = tag.get_attr(x)
            tag.set_attr(x, u)
    # ---
    new_text = parsed_page.string
    # ---
    return new_text


if __name__ == "__main__":
    text = """
    <ref name=Stat2022>{{cite journal |last1=Sapra |first1=A |last2=Bhandari |first2=P |title=Chronic Fatigue Syndrome |date=January 2022 |pmid=32491608|journal=StatPearls}}</ref>
    <ref name="Stat2022x">{{Cite journal|last2=Bhandari |first2=P |title=Chronic Fatigue Syndrome |date=January 2022 |pmid=32491608|journal=StatPearls|last=Sapra|first=A}}</ref>
    <ref name='sdsd'>{{Cite journal|last2=Bhandari |first2=P |title=Chronic Fatigue Syndrome |date=January 2022 |pmid=32491608|journal=StatPearls|last=Sapra|first=A}}</ref>

    <ref name="Stat20223"/>
    <ref name=RH2019/>
    """

    new_text = fix_ref_names(text)

    printe.showDiff(text, new_text + "\n\n")
