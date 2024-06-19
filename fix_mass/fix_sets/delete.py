"""
python3 core8/pwb.py fix_mass/fix_sets/delete
"""
from newapi.ncc_page import NEW_API

list_to_delete = [
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 1).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 10).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 11).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 12).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 13).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 14).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 2).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 3).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 4).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 5).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 6).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 7).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 8).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80302 None 9).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 1).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 10).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 11).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 12).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 13).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 14).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 15).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 16).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 17).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 18).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 19).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 2).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 20).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 21).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 22).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 23).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 24).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 25).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 3).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 4).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 5).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 6).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 7).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 8).JPG",
    "File:Ankle x-ray - labeling questions (Radiopaedia 70242-80303 None 9).JPG",
]



api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()


for x in list_to_delete:
    params = {
        "action": "delete",
        "format": "json",
        "title": x,
        "reason": "Duplicate",
        "formatversion": "2"
    }
    # ---
    result = api_new.post_params(params, addtoken=True)
    # ---
    print(result)
