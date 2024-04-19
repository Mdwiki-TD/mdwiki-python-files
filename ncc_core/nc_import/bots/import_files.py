"""

bot for importing files from nccommons to wikipedia

"""
import re
from newapi import printe
from nc_import.api_bots.ncc_page import ncc_MainPage, ncc_NEW_API
from nc_import.bots import upload_file
from nc_import.bots.db import add_to_db, add_to_jsonl

# add_to_db(title, code)
# add_to_jsonl({"lang": code, "title": title})

# upload = upload_file.upload_by_url(file_name, text, url, comment='', code="en", family="wikipedia")


def get_file_text(title):
    """
    Retrieves the text content of a file from NC Commons.
    """
    title = f"File:{title}" if not title.startswith("File:") else title
    printe.output(f"<<yellow>>get_file_text: {title} from nccommons:")

    page = ncc_MainPage(title, "www", family="nccommons")
    text = page.get_text()

    return text


def categories_work(text):
    """
    remove all categories from the text
    """
    # ---
    text = re.sub(r"\[\[Category:(.*?)\]\]", "", text, flags=re.DOTALL)
    # ---
    text += "\n[[Category:Files imported from NC Commons]]"
    # ---
    return text


def import_file(title, code):
    """
    Imports a file from NC Commons to Wikipedia.
    """
    printe.output(f"<<yellow>>import_file: File:{title} to {code}wiki:")
    # ---
    file_text = get_file_text(title)
    # ---
    file_text = categories_work(file_text)
    # ---
    api_new = ncc_NEW_API("www", family="nccommons")
    # api_new.Login_to_wiki()
    img_url = api_new.Get_image_url(title)
    # ---
    upload = upload_file.upload_by_url(title, file_text, img_url, comment="Bot: import from nccommons.org", code=code, family="wikipedia")
    # ---
    if upload:
        printe.output(f"<<lightgreen>>File:{title} imported to {code}wiki.")
        add_to_db(title, code)
        add_to_jsonl({"lang": code, "title": title})
    # ---
    return upload
