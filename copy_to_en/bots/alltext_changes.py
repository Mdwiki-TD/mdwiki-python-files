"""
python3 core8/pwb.py copy_to_en/alltext_changes

Usage:
from copy_to_en import alltext_changes

"""
import re
from newapi import printe
import wikitextparser as wtp
from copy_to_en.bots import text_changes


def change_last_Section(section):
    # del all categories
    text = section.contents
    # ---
    for cat in section.wikilinks:
        # print(cat)
        if str(cat).startswith("[[Category:"):
            text = text.replace(str(cat), "")

    text = re.sub(r"\n+", "\n", text)

    # del all langlinks

    for line in text.split("\n"):
        line2 = line.strip()
        patern = r"\[\[[a-z-]+:[^\]\n]+\]\]"
        matches = re.findall(patern, line2)
        for m in matches:
            text = text.replace(m, "")

    return text


def do_alltext_changes(text):
    parsed = wtp.parse(text)
    # get the last Section
    last_Section = ""
    for section in reversed(parsed.sections):
        last_Section = section
        break

    last_new = change_last_Section(last_Section)

    text = text.replace(last_Section.contents, last_new)

    return text


def do_all_text(alltext, revid, unlinkedwikibase):
    # ---
    revid_temp = f"{{{{mdwiki revid|{revid}}}}}"
    # ---
    alltext = text_changes.do_text_fixes(alltext)
    # ---
    alltext = do_alltext_changes(alltext)
    # ---
    alltext += "\n[[Category:Mdwiki Translation Dashboard articles/fulltext]]"
    # ---
    alltext = f"{unlinkedwikibase}\n{revid_temp}\n{alltext}"
    # ---
    return alltext


if __name__ == "__main__":
    tet = """
{{#unlinkedwikibase:id=Q273510}}{{Redirect|Yeast infection|yeast infections affecting the vagina|vaginal yeast infection}}{{For|the invasive form of Candidiasis|Candidemia}}
{{short description|fungal infection due to any type of Candida}}
{{Infobox medical condition
| name            = Candidiasis
| synonym         = Candidosis, moniliasis, oidiomycosis<ref name="Andrews"/>
| image           = Human tongue infected with oral candidiasis.jpg
| image_size      =
| image_thumbtime =
| alt             = Photo of a light-skinned human sticking tongue out where the tongue is mostly colored light yellow due to an oral candidiasis infection
| caption         = Oral candidiasis (thrush)
| pronounce       =
| field           = [[Infectious diseases (medical specialty)|Infectious disease]]<ref name=ICD-11>{{cite web |title=ICD-11 - ICD-11 for Mortality and Morbidity Statistics |url=https://icd.who.int/browse11/l-m/en#/http%3a%2f%2fid.who.int%2ficd%2fentity%2f2055968951 |website=icd.who.int |access-date=26 June 2021 |archive-date=1 August 2018 |archive-url=https://archive.today/20180801205234/https://icd.who.int/browse11/l-m/en%23/http://id.who.int/icd/entity/294762853#/http%3a%2f%2fid.who.int%2ficd%2fentity%2f2055968951 |url-status=live }}</ref>
| symptoms        = White patches or vaginal discharge, itchy<ref name=CDCVaginal2019/><ref name=CDCThrush2019/>
| complications   =
| onset           =
| duration        =
| types           =
| causes          = ''[[Candida (fungus)|Candida]]'' (a type of [[yeast]])<ref name=CDCCan2019/>
| risks           = Immunosuppression ([[HIV/AIDS]]), [[diabetes]], [[corticosteroid]]s, [[antibiotic]] therapy<ref name=CDC2014RiskO/>
| diagnosis       =
| differential    =
| prevention      =
| treatment       =
| medication      = [[Clotrimazole]], [[nystatin]], [[fluconazole]]<ref name=CDC2014Otx/>
| prognosis       =
| frequency       = 6% of babies (mouth)<ref name=Oral2014Stat/> 75% of women at some time (vaginal)<ref name=CDC2014Epi/>
| deaths          =
| video1          = [[File:Candidal infections.webm|frameless|upright=1.36|Video explanation]]
}}
<!-- Definition and symptoms -->
'''Candidiasis''' is a [[fungal infection]] due to any type of ''[[Candida (fungus)|Candida]]'' (a type of [[yeast]]).<ref name=CDCCan2019>{{Cite web|url=https://www.cdc.gov/fungal/diseases/candidiasis/|title=Candidiasis|last=|first=|date=13 November 2019|website=Fungal Diseases|publisher=Centers for Disease Control and Prevention|url-status=live|archive-url=https://web.archive.org/web/20141229221331/http://www.cdc.gov/fungal/diseases/candidiasis/|archive-date=29 December 2014|access-date=24 Dec 2019|location=United States}}</ref> When it [[Oral candidiasis|affects the mouth]], in some countries it is commonly called '''thrush'''.<ref name=CDCThrush2019/> Signs and symptoms include white patches on the tongue or other areas of the mouth and throat.<ref name=CDCThrush2019>{{Cite web|url=https://www.cdc.gov/fungal/diseases/candidiasis/thrush/index.html|title=Candida infections of the mouth, throat, and esophagus|last=|first=|date=13 November 2019|website=Fungal Diseases|publisher=Centers for Disease Control and Prevention|url-status=live|archive-url=https://web.archive.org/web/20190109142756/https://www.cdc.gov/fungal/diseases/candidiasis/thrush/index.html|archive-date=9 January 2019|access-date=24 Dec 2019|location=United States}}</ref> Other symptoms may include soreness and problems swallowing.<ref name=CDC2014OralS>{{cite web|title=Symptoms of Oral Candidiasis|url=https://www.cdc.gov/fungal/diseases/candidiasis/thrush/symptoms.html|website=cdc.gov|access-date=28 December 2014|date=February 13, 2014|url-status=live|archive-url=https://web.archive.org/web/20141229221255/http://www.cdc.gov/fungal/diseases/candidiasis/thrush/symptoms.html|archive-date=29 December 2014}}</ref> When it [[vaginal yeast infection|affects the vagina]], it may be referred to as a '''yeast infection''' or '''thrush'''.<ref name=CDCVaginal2019>{{Cite web|url=https://www.cdc.gov/fungal/diseases/candidiasis/genital/index.html|title=Vaginal Candidiasis|last=|first=|date=13 November 2019|website=Fungal Diseases|publisher=Centers for Disease Control and Prevention|location=United States|url-status=live|archive-url=https://web.archive.org/web/20141229221412/http://www.cdc.gov/fungal/diseases/candidiasis/genital/index.html|archive-date=29 December 2014|access-date=24 Dec 2019}}</ref><ref>{{cite web |title=Thrush in men and women |url=https://www.nhs.uk/conditions/thrush-in-men-and-women/ |website=nhs.uk |accessdate=16 March 2020 |language=en |date=9 January 2018 |archive-date=25 September 2018 |archive-url=https://web.archive.org/web/20180925180408/https://www.nhs.uk/conditions/thrush-in-men-and-women/ |url-status=live }}</ref> Signs and symptoms include genital itching, burning, and sometimes a white "cottage cheese-like" discharge from the vagina.<ref name=CDC2014VagS /> Yeast infections of the penis are less common and typically present with an itchy rash.<ref name=CDC2014VagS>{{cite web|title=Symptoms of Genital / Vulvovaginal Candidiasis|url=https://www.cdc.gov/fungal/diseases/candidiasis/genital/symptoms.html|website=cdc.gov|access-date=28 December 2014|date=February 13, 2014|url-status=live|archive-url=https://web.archive.org/web/20141229221253/http://www.cdc.gov/fungal/diseases/candidiasis/genital/symptoms.html|archive-date=29 December 2014}}</ref> Very rarely, yeast infections may become invasive, spreading to other parts of the body.<ref name=CDC2014Inv/> This may result in [[fever]]s along with other symptoms depending on the parts involved.<ref name=CDC2014Inv>{{cite web|title=Symptoms of Invasive Candidiasis|url=https://www.cdc.gov/fungal/diseases/candidiasis/invasive/symptoms.html|website=cdc.gov|access-date=28 December 2014|date=February 13, 2014|url-status=live|archive-url=https://web.archive.org/web/20141229230002/http://www.cdc.gov/fungal/diseases/candidiasis/invasive/symptoms.html|archive-date=29 December 2014}}</ref>

==See also==
*[[List of types of fungal infection]]

== References ==
{{Reflist}}

== External links ==
* {{Curlie|Health/Conditions_and_Diseases/Infectious_Diseases/Fungal/Candida/}}
* {{cite web | url = https://medlineplus.gov/yeastinfections.html | publisher = U.S. National Library of Medicine | work = MedlinePlus | title = Yeast Infections | access-date = 2020-07-06 | archive-date = 2020-06-19 | archive-url = https://web.archive.org/web/20200619202733/https://medlineplus.gov/yeastinfections.html | url-status = live }}

{{Medical resources
|  DiseasesDB     = 1929
|  ICD10          = {{ICD10|B|37||b|35}}
|  ICD9           = {{ICD9|112}}
|  ICDO           =
|  OMIM           =
|  MedlinePlus    = 001511
|  eMedicineSubj  = med
|  eMedicineTopic = 264
|  eMedicine_mult = {{eMedicine2|emerg|76}} {{eMedicine2|ped|312}} {{eMedicine2|derm|67}}
|  MeshID         = D002177
}}
{{Diseases of the skin and appendages by morphology}}
{{Mycoses}}
{{Authority control}}

[[Category:Animal fungal diseases]]
[[Category:Bird diseases]]
[[Category:Bovine diseases]]
[[Category:Horse diseases]]
[[Category:Mycosis-related cutaneous conditions]]
[[Category:Sheep and goat diseases]]
[[Category:RTT]]
[[Category:RTTEM]]


[[Category:Medical conditions related to obesity]]
[[Category:Stomach disorders]]
[[Category:RTT]]
[[Category:RTTNEURO]]
[[azb:گاسترو ایزوفاجال رفلکس مریضلیگی]]
[[Category:Mdwiki Translation Dashboard articles/fulltext]]

"""
    # ---
    newtext = do_alltext_changes(tet)
    printe.showDiff(tet, newtext)
    # ---
