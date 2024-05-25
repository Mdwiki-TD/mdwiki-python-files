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
# ---
from newapi import printe
from nccommons import api_upload
from newapi.ncc_page import NEW_API

api_new = NEW_API('www', family='nccommons')
api_new.Login_to_wiki()
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
Save_all = {1: False}

def py_input(s):
    printe.output(s)
    sa = input()
    # ---
    return sa

def do_post(params):
    # ---
    params['format'] = 'json'
    params['utf8'] = 1
    # ---
    json1 = api_new.post_params(params, addtoken=True)
    # ---
    return json1

def Get_All_pages(start, namespace="0", limit="max", apfilterredir='', limit_all=0):
    return api_new.Get_All_pages(start=start, namespace=namespace, limit=limit, apfilterredir=apfilterredir, limit_all=limit_all)

def upload_by_url(file_name, text, url, comment='', return_file_name=False, do_ext=False):
    return api_upload.upload_by_url(file_name, text, url, comment=comment, return_file_name=return_file_name, do_ext=do_ext)

def upload_by_file(file_name, text, url, comment="", code="en", family="wikipedia"):
    return api_upload.upload_by_file(file_name, text, url, comment=comment, code=code, family=family)

def create_Page(text, title, summary="create page"):
    printe.output(f" create Page {title}:")
    time_sleep = 0
    # ---
    params = {"action": "edit", "title": title, "text": text, "summary": summary, "notminor": 1, "createonly": 1}
    # ---
    if not Save_all[1] and ("ask" in sys.argv and "save" not in sys.argv):
        if 'nodiff' not in sys.argv:
            printe.output(text)
        sa = py_input(f"<<lightyellow>> nccommons.py: create:\"{title}\" page ? ([y]es, [N]o)")
        # ---
        if sa.strip() not in yes_answer:
            printe.output("<<lightred>> wrong answer")
            return False
        # ---
        if sa.strip() == "a":
            printe.output("---------------------------------------------")
            printe.output("nccommons.py create_Page save all without asking.")
            printe.output("---------------------------------------------")
            Save_all[1] = True
        # ---
    # ---
    result = do_post(params)
    # ---
    upload_result = result.get("edit", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", '')
    # ---
    if success:
        printe.output(f"** true ..  [[{title}]] ")
        printe.output(f"Done True... time.sleep({time_sleep}) ")
        time.sleep(time_sleep)
        return True
    elif error != {}:
        printe.output(f"<<lightred>> error when create_Page, error_code:{error_code}")
        printe.output(error)
    else:
        printe.output(result)
        return False
    # ---
    # printe.output("end of create_Page def return False title:(%s)" % title)
    # ---
    return False

def Find_pages_exists_or_not(liste):
    return api_new.Find_pages_exists_or_not(liste)

if __name__ == '__main__':
    print(Get_All_pages('', limit='10', limit_all=10))
