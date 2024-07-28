import sys
import re

# ---
from apis import mdwiki_api
from mdapi_sql import sql_for_mdwiki
from newapi import printe
from apis import cat_cach

link_regex = re.compile(r"\[\[(.*?)\]\]")
refreg = re.compile(r"(<ref[^>]*>[^<>]+</ref>|<ref[^>]*\/\s*>)")
reg_links_with_allise = re.compile(r"(\[\[[^\]|[<>{}]*)\|(.*?)\]\]")
reg_full_links = re.compile(r"(\[\[(?:[^][|]+)\|*(?:[^][]*(?:\[\[[^][]+\]\][^][]*)*)\]\])")
reg_templates = re.compile(r"{{(?:msg:)?(?P<name>[^{\|]+?)" r"(?:\|(?P<params>[^{]+?(?:{[^{]+?}[^{]*?)?)?)?}}")


def get_valid_Links(words_tab):
    # ---
    vav = cat_cach.Cat_Depth("Category:RTT", depth=2, ns="all")
    # ---
    if "newpages" in sys.argv:
        vav2 = vav
        vav = [t for t in vav2 if (t not in words_tab or words_tab[t] < 50)]
        # ---
        printe.output(f"Category-members:{len(vav2)}, New-members:{len(vav)}")
    # ---
    elif "sql" in sys.argv:
        vav2 = sql_for_mdwiki.get_all_pages()
        vav = [t for t in vav2 if (t not in words_tab or words_tab[t] < 50)]
        printe.output(f"ALL SQL LINKS:{len(vav2)}, to work:{len(vav)}")
    # ---
    elif "oldway" in sys.argv:
        ptext = mdwiki_api.GetPageText("WikiProjectMed:List")
        for m2 in link_regex.finditer(ptext):
            sa = re.compile(r"\[\[(\:|)(\w{2}|\w{3}|w|en|image|file|category|template)\:", flags=re.IGNORECASE)
            sal = sa.findall(m2.group(0))
            if not sal:
                itemu = m2.group(1).split("|")[0].strip()
                itemu = itemu[0].upper() + itemu[1:]
                vav.append(itemu)
        # ---
        printe.output("Get vaild_links fromlist : WikiProjectMed:List (oldway)")
    # ---
    elif "listnew" in sys.argv:
        printe.output("Get vaild_links listnew")
        ttt = """Lymphogranuloma venereum"""
        vav = [x.strip() for x in ttt.split("\n") if x.strip() != ""]
    # ---
    elif "fromlist" in sys.argv:
        vav = mdwiki_api.Get_page_links("WikiProjectMed:List")
        vav = vav.get("links", {}).keys()
        printe.output("Get vaild_links fromlist : WikiProjectMed:List")
    # ---
    else:
        printe.output("Get vaild_links from cat : RTT")
    # ---
    for x in vav[:]:
        if x.startswith("Category:"):
            vav.remove(x)
    # ---
    printe.output(f"len of vaild_links: {len(vav)}")
    # ---
    return vav


# ---
