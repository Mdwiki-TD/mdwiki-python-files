import re
from newapi.ncc_page import MainPage as ncc_MainPage

def update_text(title, text):
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    # ---
    # get * Findings: CT
    Findings = re.findall(r"\* Findings: (.*?)\n", p_text)
    if Findings:
        Findings = Findings[0]
        if Findings != '':
            text = text.replace("* Author location:", f"* Findings: {Findings}\n* Author location:")
    # ---
    # get * Modality: CT
    Modality = re.findall(r"\* Modality: (.*?)\n", p_text)
    if Modality:
        Modality = Modality[0]
        if Modality != '':
            text = text.replace("* Modality: ", f"* Modality: {Modality}")
    # ---
    if p_text.find("Category:Uploads by Fæ") != -1:
        text = text.replace("[[Category:Uploads by Mr. Ibrahem", "[[Category:Uploads by Fæ")
    # ---
    if p_text != text:
        page.save(newtext=text, summary="update")
