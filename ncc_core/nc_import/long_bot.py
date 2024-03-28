"""
This module contains functions and classes for importing files from NC Commons to Wikipedia, particularly for use by a bot.
"""
import re
import sys
import urllib.request
import wikitextparser as wtp

sys.argv.append("botuser")

from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage, NEW_API as ncc_NEW_API
from newapi.wiki_page import NEW_API, MainPage


def download_file(url):
    try:
        # Download the file to a temporary location
        temp_file_path, _ = urllib.request.urlretrieve(url)
        print(f"File downloaded to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        return None


def do_post(code, family, params, files=None):
    api_new = NEW_API(code, family=family)
    api_new.Login_to_wiki()
    # ---
    if files:
        result = api_new.post_params(params, addtoken=True, files=files)
    else:
        result = api_new.post_params(params, addtoken=True)
    # ---
    return result


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
    result = do_post(code, family, params, files={"file": open(file_path, "rb")})
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")
    error_info = result.get("error", {}).get("info", "")
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
    result = do_post(code, family, params)
    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")
    error_info = result.get("error", {}).get("info", "")
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
    errors = ["copyuploadbaddomain", "copyuploaddisabled"]
    if error_code in errors or " url " in error_info.lower():
        return upload_by_file(file_name, text, url, comment=comment, code=code, family=family)
    # ----
    return False


class PageWork:
    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.temps = []
        self.page = MainPage(self.title, self.code, family="wikipedia")
        self.text = self.page.get_text()
        self.new_text = self.text

    def start(self):
        # ---
        if not self.page.exists():
            print(f"self.page {self.page} not exists!")
            return
        # ---
        self.get_temps()
        self.work_on_temps()
        self.save()

    def get_temps(self):
        # ---
        parsed = wtp.parse(self.text)
        # ---
        for temp in parsed.templates:
            # ---
            name = str(temp.normal_name()).strip().lower().replace("_", " ")
            # ---
            if name == "nc":
                self.temps.append(temp)
        # ---
        printe.output(f"{len(self.temps)} temps")

    def work_one_temp(self, temp):
        # args = temp.arguments
        # ---
        text = temp.string
        # ---
        file_name = ""
        caption = ""
        # ---
        if temp.get_arg("1"):
            file_name = temp.get_arg("1").value
        # ---
        if temp.get_arg("2"):
            caption = temp.get_arg("2").value
        # ---
        printe.output(f"<<purple>> File:<<default>> {file_name}")
        printe.output(f"<<purple>> caption:<<default>> {caption}")
        # ---
        done = import_file(file_name, self.code)
        # ---
        if done:
            new_temp = f"[[File:{file_name}|thumb|{caption}]]"
            return new_temp
        # ---
        return text

    def work_on_temps(self):
        # ---
        for temp in self.temps:
            string = temp.string
            # ---
            # {{NC|file name from NC Commons|caption}}
            temp_new_text = self.work_one_temp(temp)
            # ---
            if temp_new_text != string:
                self.new_text = self.new_text.replace(string, temp_new_text)

    def save(self):
        if self.new_text != self.text:
            self.page.save(newtext=self.new_text, summary="bot: fix NC")


def work_on_pages(code, pages):
    for numb, page_title in enumerate(pages, 1):
        print(f"{numb=}: {page_title=}:")
        bot = PageWork(code, page_title)
        bot.start()


def get_file_text(title):
    title = f"File:{title}" if not title.startswith("File:") else title
    printe.output(f"<<yellow>>get_file_text: {title} from nccommons:")

    page = ncc_MainPage(title, "www", family="nccommons")
    text = page.get_text()

    return text


def import_file(title, code):
    printe.output(f"<<yellow>>import_file: File:{title} to {code}wiki:")
    # ---
    file_text = get_file_text(title)
    # ---
    api_new = ncc_NEW_API("www", family="nccommons")
    # api_new.Login_to_wiki()
    img_url = api_new.Get_image_url(title)
    # ---
    upload = upload_by_url(title, file_text, img_url, comment="Bot: import from nccommons.org", code=code, family="wikipedia")
    # ---
    return upload


def get_pages(code):
    api_new = NEW_API(code, family="wikipedia")

    api_new.Login_to_wiki()

    pages = api_new.Get_template_pages("Template:NC", namespace="*", Max=10000)

    return pages


def get_text():
    title = "User:Mr. Ibrahem/import bot"
    page = ncc_MainPage(title, "www", family="nccommons")
    text = page.get_text()
    # match all langs like: * ar\n* fr
    # ---
    return text


def get_langs_codes():
    text = get_text()
    langs = []
    fi = re.findall(r"\* (.*)\n", text)
    for i in fi:
        langs.append(i.strip())
    # ---
    printe.output(f"langs: {langs}")
    return langs


def start():
    """
    A function that starts the process by iterating over languages, getting pages for each language, and then working on those pages.
    """
    langs = get_langs_codes()
    # ---
    for code in langs:
        pages = get_pages(code)
        work_on_pages(code, pages)


if __name__ == "__main__":
    start()
