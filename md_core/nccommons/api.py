#!/usr/bin/python3
"""
python3 core8/pwb.py nccommons/api
Usage:
# ---
from nccommons import api
# newpages = api.Get_All_pages(start="", namespace="0", limit="max", apfilterredir="", limit_all="")
# new = api.create_Page(text=, title)
# exists = api.Find_pages_exists_or_not(titles)
# upload = api.upload_by_url(file_name, text, url, comment='')
# ---
"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
import sys
import time
import pywikibot
# ---
from newapi.ncc_page import NEW_API
api_new  = NEW_API('www', family='nccommons')
# json1    = api_new.post_params(params, addtoken=False)
api_new.Login_to_wiki()
# pages    = api_new.Find_pages_exists_or_not(liste)
# json1    = api_new.post_params(params, addtoken=False)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='', three_houers=False)
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# revisions= api_new.get_revisions(title)
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
Save_all = {1: False}
upload_all = {1: False}
# ---
def py_input(s):
    pywikibot.output(s)
    sa = input()
    # ---
    return sa

def post_s(params, addtoken=False):
    # ---
    params['format'] = 'json'
    params['utf8'] = 1
    # ---
    json1 = api_new.post_params(params, addtoken=True)
    # ---
    return json1

def Get_All_pages(start, namespace="0", limit="max", apfilterredir='', limit_all=0):
    return api_new.Get_All_pages(start=start, namespace=namespace, limit=limit, apfilterredir=apfilterredir, limit_all=limit_all)

def upload_by_url(file_name, text, url, comment='', return_file_name=False):
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    params = {'action': 'upload', 'format': 'json', 'filename': file_name, 'url': url, 'comment': comment, 'text': text}
    # ---
    if not upload_all[1] and "ask" in sys.argv:
        if 'nodiff' not in sys.argv:
            pywikibot.output(text)
        sa = py_input(f"<<lightyellow>> nccommons.py: upload file:'{file_name}' ? ([y]es, [N]o)")
        # ---
        if sa.strip() not in yes_answer:
            pywikibot.output("<<lightred>> wrong answer")
            return file_name
        # ---
        if sa.strip() == "a":
            pywikibot.output("---------------------------------------------")
            pywikibot.output("nccommons.py upload_by_url save all without asking.")
            pywikibot.output("---------------------------------------------")
            upload_all[1] = True
        # ---
    # ---
    result = post_s(params, addtoken=True)
    # ---
    # {'upload': {'result': 'Success', 'filename': 'Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'imageinfo': {'timestamp': '2023-11-29T20:12:26Z', 'user': 'Mr. Ibrahem', 'userid': 13, 'size': 52289, 'width': 506, 'height': 379, 'parsedcomment': '', 'comment': '', 'html': '', 'canonicaltitle': 'File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg', 'url': 'https://nccommons.org/media/f/fd/Pediculosis_Palpebrarum_%28Dermatology_Atlas_1%29.jpg', 'descriptionurl': 'https://nccommons.org/wiki/File:Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'sha1': '1df195d80a496c6aadcefbc6d7b8adf13caddafc', 'metadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}, {'name': 'MEDIAWIKI_EXIF_VERSION', 'value': 2}], 'commonmetadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}], 'extmetadata': {'DateTime': {'value': '2023-11-29T20:12:26Z', 'source': 'mediawiki-metadata', 'hidden': ''}, 'ObjectName': {'value': 'Pediculosis Palpebrarum (Dermatology Atlas 1)', 'source': 'mediawiki-metadata', 'hidden': ''}}, 'mime': 'image/jpeg', 'mediatype': 'BITMAP', 'bitdepth': 8}}}
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", '')
    # ---
    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [''])[0].replace("_", " ")
    # ---
    if success:
        pywikibot.output(f"<<lightgreen>> ** true .. [[File:{file_name}]] ")
        return True if not return_file_name else file_name

    elif duplicate and return_file_name:
        pywikibot.output(f"<<lightred>> ** duplicate file:  {duplicate}.")
        return f'{duplicate}' if return_file_name else True
    elif error != {}:
        pywikibot.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        pywikibot.output(error)
    # ---
    pywikibot.output(result)
    return False if not return_file_name else ''


def create_Page(text, title, summary="create page"):
    pywikibot.output(f" create Page {title}:")
    time_sleep = 0
    # ---
    params = {"action": "edit", "title": title, "text": text, "summary": summary, "notminor": 1, "createonly": 1}
    # ---
    if not Save_all[1] and ("ask" in sys.argv and "save" not in sys.argv):
        if 'nodiff' not in sys.argv:
            pywikibot.output(text)
        sa = py_input(f"<<lightyellow>> nccommons.py: create:\"{title}\" page ? ([y]es, [N]o)")
        # ---
        if sa.strip() not in yes_answer:
            pywikibot.output("<<lightred>> wrong answer")
            return False
        # ---
        if sa.strip() == "a":
            pywikibot.output("---------------------------------------------")
            pywikibot.output("nccommons.py create_Page save all without asking.")
            pywikibot.output("---------------------------------------------")
            Save_all[1] = True
        # ---
    # ---
    result = post_s(params, addtoken=True)
    # ---
    upload_result = result.get("edit", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", '')
    # ---
    if success:
        pywikibot.output(f"** true ..  [[{title}]] ")
        pywikibot.output("Done True... time.sleep(%d) " % time_sleep)
        time.sleep(time_sleep)
        return True
    elif error != {}:
        pywikibot.output(f"<<lightred>> error when create_Page, error_code:{error_code}")
        pywikibot.output(error)
    else:
        pywikibot.output(result)
        return False
    # ---
    # pywikibot.output("end of create_Page def return False title:(%s)" % title)
    # ---
    return False


def Find_pages_exists_or_not(liste):
    return api_new.Find_pages_exists_or_not(liste)

if __name__ == '__main__':
    Get_All_pages('', limit='10', limit_all=10)
