"""

from fix_mass.fix_sets.bots.find_from_url import find_file_name_from_url

"""
import jsonlines
# import os
from pathlib import Path
from newapi.ncc_page import NEW_API
from newapi import printe


api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

jsons_dir = Path(__file__).parent.parent / "jsons"

url_to_file_file = jsons_dir / "find_from_url.jsonl"

if not url_to_file_file.exists():
    url_to_file_file.write_text('{"url": "", "file_name": ""}')

data = jsonlines.open(url_to_file_file)
data = {d["url"]: d["file_name"] for d in data}


def append_data(url, file_name):
    data[url] = file_name
    # ---
    with jsonlines.open(url_to_file_file, mode="a") as writer:
        writer.write({"url": url, "file_name": file_name})


def get_from_api(url):
    # ---
    params = {"action": "upload", "format": "json", "filename": "Wiki.jpg", "url": url, "stash": 1, "formatversion": "2"}
    # ---
    # { "upload": { "result": "Warning", "warnings": { "duplicate": [ "Angiodysplasia_-_cecal_active_bleed_(Radiopaedia_168775-136954_Coronal_91).jpeg" ] }, "filekey": "1b00hc5unqxw.olk8pi.13.", "sessionkey": "1b00hc5unqxw.olk8pi.13." } }
    # ---
    data = api_new.post_params(params)
    # ---
    duplicate = data.get("upload", {}).get("warnings", {}).get("duplicate", [])
    # ---
    if not duplicate:
        return ""
    # ---
    du = "File:" + duplicate[0]
    du = du.replace("_", " ")
    # ---
    printe.output(f"find_file_name_from_url: {du}")
    # ---
    return du


def find_file_name_from_url(url):
    na = ""
    if url in data:
        printe.output(f"find_file_name_from_url: {data[url]}")
        return data[url]
    # ---
    na = get_from_api(url)
    # ---
    if na:
        append_data(url, na)
    # ---
    return na
