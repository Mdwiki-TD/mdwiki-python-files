import sys
import re
import os
from newapi.ncc_page import MainPage as ncc_MainPage
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
    # Read the contents of the existing README.md file
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Add a description of the new features and any new commands that have been added
    new_features = """
    New Features:
    - Feature 1: Description of feature 1.
    - Feature 2: Description of feature 2.
    
    New Commands:
    - Command 1: Description of command 1.
    - Command 2: Description of command 2.
    """

    # Update the README.md file with the new content
    updated_content = re.sub(r"(?<=## Features\n)", new_features, readme_content)

    # Write the updated README.md content back to the file
    with open("README.md", "w") as f:
        f.write(updated_content)
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
