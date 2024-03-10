"""

bot for importing files from nccommons to wikipedia

"""
import sys
# ---
# from newapi.wiki_page import MainPage, NEW_API
from newapi.ncc_page import MainPage as ncc_MainPage, NEW_API as ncc_NEW_API
from newapi import printe
# ---
from nc_import.bots import upload_file
# upload = upload_file.upload_by_url(file_name, text, url, comment='', code="en", family="wikipedia")

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
    api_new  = ncc_NEW_API('www', family='nccommons')
    # api_new.Login_to_wiki()
    img_url = api_new.Get_image_url(title)
    # ---
    upload = upload_file.upload_by_url(title, file_text, img_url, comment='Bot: import from nccommons.org', code=code, family="wikipedia")
    # ---
    return upload
