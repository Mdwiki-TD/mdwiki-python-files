import sys
import re
from newapi.ncc_page import MainPage as ncc_MainPage

skips = [
    "File:Benign enlargement of subarachnoid spaces (Radiopaedia 25801-25990 Coronal 1).jpg"
]

def get_ta(text, ta):
    res = re.findall(rf"\* {ta}: (.*?)\n", text)
    if res:
        res = res[0]
        return res
    return ""

def update_text(title, text):
    # ---
    if title in skips:
        return
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    # ---
    # get * Findings: CT
    Findings = get_ta(p_text, "Findings")
    if Findings != '':
        text = text.replace("* Author location:", f"* Findings: {Findings}\n* Author location:")
    # ---
    # get * Study findings:
    Study_findings = get_ta(p_text, "Study findings")
    if Study_findings != '':
        text = text.replace("* Author location:", f"* Study findings: {Study_findings}\n* Author location:")
    # ---
    Modality = get_ta(p_text, "Modality")
    if Modality != '':
        text = text.replace("* Modality: ", f"* Modality: {Modality}")
    # ---
    ASK = "Category:Uploads by Fæ" in p_text and "askusa" in sys.argv
    # ---
    if p_text.find("Category:Uploads by Fæ") != -1:
        text = text.replace("[[Category:Uploads by Mr. Ibrahem", "[[Category:Uploads by Fæ")
    # ---
    if p_text != text:
        page.save(newtext=text, summary="update", ASK=ASK)
    # ---
    skips.append(title)
