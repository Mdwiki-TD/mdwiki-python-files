"""
python3 core8/pwb.py copy_to_en/text_changes

Usage:
from copy_to_en import text_changes# text = text_changes.work(text)

"""

import logging
import re

import wikitextparser as wtp
from copy_to_en.bots.fix_refs_names import fix_ref_names

logger = logging.getLogger(__name__)

temps_to_delete = [
    "short description",
    "toc limit",
    "use american english",
    "use dmy dates",
    "sprotect",
    "about",
    "featured article",
    "redirect",
    "#unlinkedwikibase",
    "anchor",
    "defaultsort",
    "distinguish",
    "esborrany",
    "fr",
    "good article",
    "italic title",
    "other uses",
    "redirect-distinguish",
    "see also",
    "tedirect-distinguish",
    "use mdy dates",
    "void",
]

temps_patterns = [
    r"^pp(-.*)?$",
    r"^articles (for|with|needing|containing).*$",
    r"^engvar[ab]$",
    r"^use[\sa-z]+(english|spelling|referencing)$",
    r"^use [dmy]+ dates$",
    r"^wikipedia articles (for|with|needing|containing).*$",
    r"^(.*-)?stub$",
    r"^.*? sidebar$",
]


def remove_images(text):
    pattern = r"\[\[(File:[^][|]+)\|([^][]*(\[\[[^][]+\]\][^][]*)*)\]\]"
    matches = re.findall(pattern, text)

    images = {}
    for link in matches:
        link, v, c = link
        print(link)
        file_name = link.split("|")[0]
        new_text = "{{" + f"subst:#ifexist:{file_name}|{link}" + "}}"
        text = text.replace(link, new_text)
        images[file_name] = link

    return text


def del_temps(text):
    """Delete specified templates from the given text.

    This function parses the input text to identify and remove specific
    templates based on their names. It first processes the templates and
    removes those that match predefined names or patterns. After that, it
    checks for any parser functions that also match the specified names for
    deletion. The result is a cleaned-up version of the input text with the
    designated templates and functions removed.

    Args:
        text (str): The input text containing templates and functions.

    Returns:
        str: The modified text with specified templates and functions removed.
    """

    # ---
    parsed = wtp.parse(text)
    for temp in parsed.templates:
        # ---
        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        if name in temps_to_delete:
            text = text.replace(temp.string.strip(), "")
        else:
            for pattern in temps_patterns:
                if re.match(pattern, name):
                    text = text.replace(temp.string.strip(), "")
                    break
    # ---
    parsed = wtp.parse(text)
    # ---
    for func in parsed.parser_functions:
        name = str(func.name).strip().lower().replace("_", " ")
        # ---
        if name in temps_to_delete:
            text = text.replace(func.string.strip(), "")
    # ---
    return text.strip()


def work(text):
    # ---
    # text = remove_images(text)
    # ---
    text = del_temps(text)
    # ---
    # text += "\n[[Category:Mdwiki Translation Dashboard articles]]"
    # ---
    return text


def do_text_fixes_newxx(newtext):
    """Process and clean up article text.

    Args:
        newtext (str): The input text to process

    Returns:
        str: Processed text with:
            - Templates and parser functions removed
            - Drugbox templates standardized to "Infobox drug"
            - Content before first infobox removed

    """
    # ---
    newtext = work(newtext)
    # ---
    # Case-insensitive template replacement
    newtext = re.sub(r"\{\{drugbox", "{{Infobox drug", newtext, flags=re.IGNORECASE)
    # ---
    # Find first occurrence of infobox
    infobox_match = re.search(r"{{(infobox|drugbox)", newtext, re.IGNORECASE)
    if infobox_match:
        prefix = newtext[: infobox_match.start()].strip()
        if prefix:
            printe.output(f"Warning: Removing content before infobox: {prefix[:100]}...")
        newtext = newtext[infobox_match.start() :]
    # ---
    return newtext


def do_text_fixes(newtext):
    newtext = work(newtext)
    # ---
    newtext = newtext.replace("{{Drugbox", "{{Infobox drug")
    newtext = newtext.replace("{{drugbox", "{{Infobox drug")
    # ---
    # remove any text before {{Infobox or {{Drugbox
    if newtext.lower().find("{{infobox") != -1:
        newtext = newtext[newtext.lower().find("{{infobox") :]
    elif newtext.lower().find("{{drugbox") != -1:
        newtext = newtext[newtext.lower().find("{{drugbox") :]
    # ---
    newtext = fix_ref_names(newtext)
    # ---
    return newtext


if __name__ == "__main__":
    tet = """{{#unlinkedwikibase:id=Q2553496}}{{Short description|Medication}}
{{Drugbox
| Verifiedfields    = changed
| verifiedrevid     = 462259703
| image             = Netilmicin structure.svg

<!-- Names -->
| pronounce         =
| tradename         = Netromycin, others
| synonyms          = 1-N-ethylsisomicin
| IUPAC_name        = (2'"R"',3'"R"',4'"R"',5'"R"')-2-{[(1''S'',2''S'',3'"R"',4''S'',6'"R"')-4-Amino-3-{[(2''S'',3'"R"')-3-amino-6-(aminomethyl)-3,4-dihydro-2''H''-pyran-2-yl]oxy}-6-(ethylamino)-2-hydroxycyclohexyl]oxy}-5-methyl-4-(methylamino)oxane-3,5-diol

<!-- Clinical data -->
| class             = [[Aminoglycoside]]<ref name=SPS2020/>
| uses              = [[Conjunctivitis]], [[urinary tract infections]]<ref name=Online2023/><ref name=Brand2023/>
| side_effects      = Eye redness or discomfort,<ref name=BNF2023/> [[hearing problems]], [[kidney problems]]<ref name=BNF2023/><ref name=Camp1989/>
| interactions      = <!-- notable interactions -->
| pregnancy_AU      = <!-- A / B1 / B2 / B3 / C / D / X -->
| pregnancy_US      = <!-- A / B / C / D / X -->
| pregnancy_category=
| breastfeeding     =
| routes_of_administration= [[Eye drop]], by injection
| onset             =
| duration_of_action=
| defined_daily_dose=
| typical_dose      =

<!-- External links -->
| Drugs.com         =
| MedlinePlus       =

<!-- Legal data -->
| legal_AU          = <!-- Unscheduled / S2 / S4 / S8 -->
| legal_UK          = POM
| legal_US          = <!-- OTC / Rx-only -->
| legal_status      =

<!-- Pharmacokinetic data -->
| bioavailability   = ~0%
| protein_bound     =
| metabolism        =
| elimination_half-life= 2.5 hours
| excretion         =

<!-- Chemical and physical data -->
| C= 21 | H= 41 | N= 5 | O= 7
| SMILES            = O[C@]3(C)[C@H](NC)[C@@H](O)[C@@H](O[C@H]2[C@H](NCC)C[C@H](N)[C@@H](OC1O\\C(=C/CC1N)CN)[C@@H]2O)OC3
| StdInChI          = 1S/C21H41N5O7/c1-4-26-13-7-12(24)16(32-19-11(23)6-5-10(8-22)31-19)14(27)17(13)33-20-15(28)18(25-3)21(2,29)9-30-20/h5,11-20,25-29H,4,6-9,22-24H2,1-3H3/t11?,12-,13+,14-,15+,16+,17-,18+,19?,20+,21-/m0/s1
| StdInChI_Ref      = {{stdinchicite|correct|chemspider}}
| StdInChIKey       = CIDUJQMULVCIBT-KALHTFJLSA-N
| StdInChIKey_Ref   = {{stdinchicite|correct|chemspider}}
}}
<!-- Definition and medical uses -->
'''Netilmicin''', sold under the brand name '''Netromycin''' among others, is an [[antibiotic]] used to treat [[conjunctivitis]] and [[urinary tract infections]] among other bacterial infections.<ref name=Online2023>{{cite web |title=eEML - Electronic Essential Medicines List |url=https://list.essentialmeds.org/medicines/653 |website=list.essentialmeds.org |accessdate=9 September 2023 |archive-date=9 June 2023 |archive-url=https://web.archive.org/web/20230609212314/https://list.essentialmeds.org/medicines/653 |url-status=live }}</ref><ref name=Brand2023>{{cite web |title=Netilmicin - brand name list from Drugs.com |url=https://www.drugs.com/ingredient/netilmicin.html |website=Drugs.com |accessdate=9 September 2023 |language=en |archive-date=6 June 2023 |archive-url=https://web.archive.org/web/20230606062117/https://www.drugs.com/ingredient/netilmicin.html |url-status=live }}</ref><ref name=Camp1989/> It is available as an [[eye drop]], and has been given by injection.<ref name=BNF2023/><ref name=Camp1989/>

<!-- Side effects and mechanism -->
Side effects may include eye redness or discomfort.<ref name=BNF2023>{{cite web |title=Netilmicin |url=https://bnf.nice.org.uk/drugs/netilmicin/ |website=NICE |publisher=BNF |accessdate=9 September 2023 |archive-date=10 September 2023 |archive-url=https://web.archive.org/web/20230910112454/https://www.nice.org.uk/bnf-uk-only |url-status=live }}</ref> Other concerns include [[hearing problems]] and [[kidney problems]].<ref name=BNF2023/><ref name=Camp1989/> Use is not recommended when [[breastfeeding]].<ref name=Camp1989/> It is an [[aminoglycoside]] and works by interfering with [[protein]] production by bacteria.<ref name=Camp1989>{{cite journal |last1=Campoli-Richards |first1=DM |last2=Chaplin |first2=S |last3=Sayce |first3=RH |last4=Goa |first4=KL |title=Netilmicin. A review of its antibacterial activity, pharmacokinetic properties and therapeutic use. |journal=Drugs |date=November 1989 |volume=38 |issue=5 |pages=703-56 |doi=10.2165/00003495-198938050-00003 |pmid=2689137}}</ref><ref name=SPS2020/>

<!-- Society and culture -->
Netilmicin was patented in 1973 and approved for medical use in 1981.<ref name=Fis2006>{{cite book |last1=Fischer |first1=Jnos |last2=Ganellin |first2=C. Robin |title=Analogue-based Drug Discovery |date=2006 |publisher=John Wiley & Sons |isbn=9783527607495 |page=508 |url=https://books.google.com/books?id=FjKfqkaKkAAC&pg=PA508 |language=en |access-date=2023-03-08 |archive-date=2023-08-26 |archive-url=https://web.archive.org/web/20230826134255/https://books.google.com/books?id=FjKfqkaKkAAC&pg=PA508 |url-status=live }}</ref> It was approved for external eye infections in the UK in 2019.<ref name=SPS2020>{{cite web | title=Netilmicin | website=SPS - Specialist Pharmacy Service | date=2 June 2020 | url=https://www.sps.nhs.uk/medicines/netilmicin/ | access-date=21 August 2020 | archive-date=24 October 2021 | archive-url=https://web.archive.org/web/20211024093227/https://www.sps.nhs.uk/medicines/netilmicin/ | url-status=live }}</ref> The eye drop is on the [[WHO Model List of Essential Medicines|World Health Organization's List of Essential Medicines]] as an alternative to [[gentamicin]].<ref name="WHO23rd">{{cite book | vauthors = ((World Health Organization)) | title = The selection and use of essential medicines 2023: web annex A: World Health Organization model list of essential medicines: 23rd list (2023) | year = 2023 | hdl = 10665/371090 | author-link = World Health Organization | publisher = World Health Organization | location = Geneva | id = WHO/MHP/HPS/EML/2023.02 | hdl-access=free }}</ref> In the United Kingdom a course of treatment costs the [[NHS about £10.<ref>{{cite web |title=Netilmicin Medicinal forms |url=https://bnf.nice.org.uk/drugs/netilmicin/medicinal-forms/ |website=NICE |publisher=BNF |accessdate=9 September 2023 |archive-date=10 September 2023 |archive-url=https://web.archive.org/web/20230910112541/https://www.nice.org.uk/bnf-uk-only |url-status=live }}</ref> It is made by [[semisynthetic|altering]] [[sisomicin]].<ref name=Camp1989/>
{{TOC limit}}
==References==
<references />
"""
    # ---
    newtext = work(tet)
    printe.showDiff(tet, newtext)
    # ---
