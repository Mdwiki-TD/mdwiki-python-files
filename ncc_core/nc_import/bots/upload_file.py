#!/usr/bin/python3
"""

Usage:
# ---
from nc_import.bots import upload_file
# upload = upload_file.upload_by_url(file_name, text, url, comment='', code="en", family="wikipedia")
# ---

"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
import requests
import urllib.request
import tempfile
import os
import sys
# ---
from newapi import printe
# ---
sys.argv.append("botuser")
# ---
from newapi.wiki_page import NEW_API
# api_new  = NEW_API('www', family='nccommons')
# api_new.Login_to_wiki()
# json1    = api_new.post_params(params, addtoken=False)


def download_file(url):
    try:
        # Download the file to a temporary location
        temp_file_path, _ = urllib.request.urlretrieve(url)
        print(f"File downloaded to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        return None


def upload_by_file(file_name, text, url, comment="", code="en", family="wikipedia"):
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    # get the file from url
    file_path = download_file(url)
    # ---
    params = {"action": "upload", "format": "json", "filename": file_name, "comment": comment, "text": text, "utf8": 1}
    # ---
    api_new = NEW_API(code, family=family)
    # api_new.Login_to_wiki()
    # ---
    result = api_new.post_params(params, addtoken=True, files={"file": open(file_path, "rb")})
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")
    error_info = result.get("error", {}).get("info", '')
    # ---
    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    # ---
    if success:
        printe.output(f"<<lightgreen>> ** upload true .. [[File:{file_name}]] ")
        return True

    if duplicate:
        printe.output(f"<<lightred>> ** duplicate file:  {duplicate}.")

    if error:
        printe.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        printe.output(error)
    
    # ----
    return False

def upload_by_url(file_name, text, url, comment="", code="en", family="wikipedia"):
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    params = {"action": "upload", "format": "json", "filename": file_name, "url": url, "comment": comment, "text": text, "utf8": 1}
    # ---
    api_new = NEW_API(code, family=family)
    api_new.Login_to_wiki()
    # ---
    result = api_new.post_params(params, addtoken=True)
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")
    error_info = result.get("error", {}).get("info", '')
    # ---
    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    # ---
    if success:
        printe.output(f"<<lightgreen>> ** true .. [[File:{file_name}]] ")
        return True

    if duplicate:
        printe.output(f"<<lightred>> ** duplicate file:  {duplicate}.")
    
    if error:
        printe.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        printe.output(error_info)
    errors = [
        "copyuploadbaddomain",
        "copyuploaddisabled"
    ]
    if error_code in errors or " url " in error_info.lower():
        return upload_by_file(file_name, text, url, comment=comment, code=code, family=family)
    # ----
    return False
