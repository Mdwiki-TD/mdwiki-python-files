"""

from fix_mass.fix_sets.name_bots.url_name_upload import find_url_file_upload

"""
import jsonlines

# from pathlib import Paths
from newapi.ncc_page import NEW_API
from newapi import printe
from fix_mass.fix_sets.jsons_dirs import jsons_dir

# from fix_mass.dp_infos.db_duplict import insert_url_file # insert_url_file(url, file)
api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()

url_to_file_file = jsons_dir / "find_from_url.jsonl"

if not url_to_file_file.exists():
    url_to_file_file.write_text('{"url": "", "file_name": ""}')

data = jsonlines.open(url_to_file_file)
data = {d["url"]: d["file_name"] for d in data}


def append_data(url, file_name):
    data[url] = file_name
    # ---
    # insert_url_file(url, file_name)
    # ---
    # with jsonlines.open(url_to_file_file, mode="a") as writer:
    #     writer.write({"url": url, "file_name": file_name})


def get_from_api(url):
    # ---
    # extension = get_image_extension(image_url)
    extension = url.split(".")[-1].lower()
    # ---
    files = {
        "jpg": "Wiki.jpg",
        "png": "Test.png",
    }
    # ---
    filename = f"Wiki.{extension}"
    # ---
    filename = files.get(extension, filename)
    # ---
    params = {"action": "upload", "format": "json", "filename": filename, "url": url, "stash": 1, "formatversion": "2"}
    # ---
    # { "upload": { "result": "Warning", "warnings": { "duplicate": [ "Angiodysplasia_-_cecal_active_bleed_(Radiopaedia_168775-136954_Coronal_91).jpeg" ] }, "filekey": "1b00hc5unqxw.olk8pi.13.", "sessionkey": "1b00hc5unqxw.olk8pi.13." } }
    # ---
    data = api_new.post_params(params)
    # ---
    duplicate = data.get("upload", {}).get("warnings", {}).get("duplicate", [])
    # ---
    du = ""
    # ---
    if duplicate:
        du = "File:" + duplicate[0]
        du = du.replace("_", " ")
        # ---
        printe.output(f"duplicate, find_url_file_upload: {du}")
    else:
        print(data)
    # ---
    return du


def find_url_file_upload(url, do_api=True):
    na = ""
    if url in data:
        da = data[url]
        if da.find("https") == -1:
            # printe.output(f"find_url_file_upload: {data[url]}")
            return da
    # ---
    if do_api:
        na = get_from_api(url)
    # ---
    if na:
        append_data(url, na)
    # ---
    return na
