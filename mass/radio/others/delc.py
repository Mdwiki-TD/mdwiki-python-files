"""

python3 core8/pwb.py mass/radio/delc ask diff


"""
import re
from newapi.ncc_page import MainPage as ncc_MainPage

cats = '''
    Category:Radiopaedia case 9951 Negative ulnar variance
    Category:Radiopaedia case 11146 Abdominal CSF pseudocyst
    Category:Radiopaedia case 11159 Achilles tendon rupture
    Category:Radiopaedia case 11160 Achondroplasia
    Category:Radiopaedia case 11161 Acute cholecystitis
    Category:Radiopaedia case 11163 Acute pancreatitis
    Category:Radiopaedia case 11176 Adrenocortical carcinoma
    Category:Radiopaedia case 11182 Amyloid arthropathy
    Category:Radiopaedia case 11197 Aortic dissection
    Category:Radiopaedia case 11205 Arachnoid cyst
    Category:Radiopaedia case 11206 Arachnoid cyst
    Category:Radiopaedia case 11219 Autoimmune hepatitis
    Category:Radiopaedia case 11249 Boxer fracture
    Category:Radiopaedia case 11258 Bronchiectasis
    Category:Radiopaedia case 11260 Bronchoalveolar carcinoma
    Category:Radiopaedia case 11301 Cholesterol granuloma
    Category:Radiopaedia case 11305 Chondrosarcoma
    Category:Radiopaedia case 11309 Choroidal effusion
    Category:Radiopaedia case 11319 Cleidocranial dysostosis
    Category:Radiopaedia case 17427 Coarctation of the aorta
    Category:Radiopaedia case 29051 Baastrup disease
    Category:Radiopaedia case 41146 Chauffeur fracture
    Category:Radiopaedia case 42764 Bony pelvis (illustrations)
    Category:Radiopaedia case 43478 Anatomy Quiz (MRI knee)
    Category:Radiopaedia case 50575 Normal radiographic anatomy of the hip
    Category:Radiopaedia case 54942 Broken cerclage wire
    Category:Radiopaedia case 56393 Calcific tendinitis (ruptured)
    Category:Radiopaedia case 69438 Normal physiological FDG uptake in lactating breasts
    Category:Radiopaedia case 76316 Arytenoid cartilages (illustration)
    Category:Radiopaedia case 79758 Nuchal cord types
    Category:Radiopaedia case 80949 Normal wrist alignment, dorsal and volar intercalated segmental instability (illustration)
    Category:Radiopaedia case 90395 Cerebellar vermis (illustration)
    Category:Radiopaedia case 11276 Cardiac pacemaker
    '''
# ---
cats = [x.strip() for x in cats.split("\n") if x.strip()]
# ---
for cat in cats:
    print(f"cat: {cat}")
    page = ncc_MainPage(cat, "www", family="nccommons")

    if not page.exists():
        continue
    text = page.get_text()
    # ---
    # remove category liike: [[Category:Radiopaedia cases by type | 011219]]
    newtext = re.sub(r"\[\[Category:Radiopaedia cases by type\s*\|*.*?\]\]", "", text)
    # ---
    if newtext == text:
        print("newtext == text")
        continue
    # ---
    page.save(newtext=newtext, summary="")
