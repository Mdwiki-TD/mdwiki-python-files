#!/usr/bin/python3
"""

Usage:
from nccommons import api_upload

def upload_by_url():
    return api_upload.upload_by_url(file_name, text, url, comment='')
# ---
"""
import sys
import urllib.request

# ---
from nccommons import ext
from nccommons import fix_svg
from newapi import printe
from newapi.ncc_page import NEW_API

api_new = NEW_API("www", family="nccommons")
yes_answer = ["y", "a", "", "Y", "A", "all"]
upload_all = {1: False}

def download_file(url):
    """
    Downloads a file from a given URL to a temporary location.
    """
    try:
        # Download the file to a temporary location
        temp_file_path, _ = urllib.request.urlretrieve(url)
        print(f"File downloaded to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        return None

def do_post(params, code="", family="", files=None):
    """
    Makes a POST request to the Wikipedia API with specified parameters.
    """
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    api_new.Login_to_wiki()
    # ---
    if files:
        result = api_new.post_params(params, addtoken=True, files=files)
    else:
        result = api_new.post_params(params, addtoken=True)
    # ---
    return result

def upload_by_file(file_name, text, url, comment="", code="en", family="wikipedia", fix_svg_dtd=False):
    """
    Uploads a file to Wikipedia using a local file.
    """
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    # get the file from url
    file_path = download_file(url)
    # ---
    if not file_path:
        printe.output(f"<<lightred>> download file failed, {url=}")
        return False
    # ---
    printe.output(f"<<lightyellow>> {file_path=}...")
    # ---
    if file_name.endswith(".svg") and fix_svg_dtd:
        file_path = fix_svg.remove_svg_dtd(file_path)
    # ---
    params = {"action": "upload", "format": "json", "filename": file_name, "comment": comment, "text": text, "utf8": 1}
    # ---
    # result = do_post(params, code=code, family=family, files={"file": open(file_path, "rb")})
    result = do_post(params, files={"file": open(file_path, "rb")})
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
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
        error_code = error.get("code", "")
        error_info = error.get("info", "")
        printe.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        printe.output(error)

    # ---
    return False


def do_ask(text, file_name):
    # ---
    if "nodiff" not in sys.argv:
        printe.output(text)
    # ---
    printe.output(f"<<lightyellow>> {__name__}: upload file:'{file_name}' ? ([y]es, [N]o)")
    sa = input()
    # ---
    if sa.strip() not in ["y", "a", "", "Y", "A", "all"]:
        printe.output("<<lightred>> wrong answer")
        return False
    # ---
    if sa.strip() == "a":
        printe.output("---------------------------------------------")
        printe.output(f"{__name__} upload_by_url save all without asking.")
        printe.output("---------------------------------------------")
        upload_all[1] = True
    # ---
    return True

def upload_by_url(file_name, text, url, comment="", return_file_name=False, do_ext=False, code="en", family="wikipedia"):
    """

    Uploads a file to Wikipedia using a URL.

    """
    # ---
    if not url:
        printe.output("<<lightred>>upload_by_url: no url")
        return False
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    params = {"action": "upload", "format": "json", "filename": file_name, "url": url, "comment": comment, "text": text, "utf8": 1}
    # ---
    if "ask" in sys.argv and not upload_all[1]:
        ask = do_ask(text, file_name)
        if not ask:
            return file_name
    # ---
    result = do_post(params)
    # ---
    # {'upload': {'result': 'Success', 'filename': 'Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'imageinfo': {'timestamp': '2023-11-29T20:12:26Z', 'user': 'Mr. Ibrahem', 'userid': 13, 'size': 52289, 'width': 506, 'height': 379, 'parsedcomment': '', 'comment': '', 'html': '', 'canonicaltitle': 'File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg', 'url': 'https://nccommons.org/media/f/fd/Pediculosis_Palpebrarum_%28Dermatology_Atlas_1%29.jpg', 'descriptionurl': 'https://nccommons.org/wiki/File:Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'sha1': '1df195d80a496c6aadcefbc6d7b8adf13caddafc', 'metadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}, {'name': 'MEDIAWIKI_EXIF_VERSION', 'value': 2}], 'commonmetadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}], 'extmetadata': {'DateTime': {'value': '2023-11-29T20:12:26Z', 'source': 'mediawiki-metadata', 'hidden': ''}, 'ObjectName': {'value': 'Pediculosis Palpebrarum (Dermatology Atlas 1)', 'source': 'mediawiki-metadata', 'hidden': ''}}, 'mime': 'image/jpeg', 'mediatype': 'BITMAP', 'bitdepth': 8}}}
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    # ---
    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    exists = upload_result.get("warnings", {}).get("exists", False)
    # ---
    if success:
        printe.output(f"<<lightgreen>> ** true .. [[File:{file_name}]] ")
        return True if not return_file_name else file_name

    if duplicate and return_file_name:
        printe.output(f"<<lightred>> ** duplicate file:  {duplicate}.")
        return f"{duplicate}" if return_file_name else True
    # ---
    if error:
        error_code = error.get("code", "")
        error_info = error.get("info", "")
        printe.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        # ---
        printe.output(f"<<lightred>> url: {url}")
        # ---
        printe.output(error)
        # ---
        errors = ["copyuploadbaddomain", "copyuploaddisabled"]
        if error_code in errors or " url " in error_info.lower():
            return upload_by_file(file_name, text, url, comment=comment, code=code, family=family)
        # ---
        if error_code == "verification-error":
            if do_ext and "MIME type of the file" in error_info:
                new_file_name = ext.get_new_ext(error_info, file_name)
                if new_file_name:
                    return upload_by_url(new_file_name, text, url, comment=comment, return_file_name=return_file_name)
            # ---
            # {'error': {'code': 'verification-error', 'info': 'Cannot upload SVG files that contain a non-standard DTD declaration.', 'details': ['upload-scripted-dtd'], '*': ''}}
            # ---
            if error_info == "Cannot upload SVG files that contain a non-standard DTD declaration.":
                return upload_by_file(file_name, text, url, comment=comment, code=code, family=family, fix_svg_dtd=True)

    # ---
    printe.output(result)
    # ---
    return False if not return_file_name else ""
