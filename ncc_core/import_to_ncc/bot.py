"""

python3 core8/pwb.py import_to_ncc/bot

"""
from newapi import printe
from newapi.wiki_page import MainPage as wiki_MainPage, NEW_API as wiki_NEW_API
from nccommons import api

from newapi.ncc_page import NEW_API as ncc_NEW_API

api_new = ncc_NEW_API("www", family="nccommons")

api_new.Login_to_wiki()

imges_liist = [
    "File:Extracted image icon.svg",
    "File:CC BY-NC-ND.svg",
]

def import_file(title):
    """
    Imports a file from Wikimedia Commons to NC Commons.
    """
    printe.output(f"<<yellow>>import_file: File:{title} to nccommons:")
    # ---
    title_file = f"File:{title}" if not title.startswith("File:") else title
    printe.output(f"<<yellow>>get_file_text: {title} from commons.wikimedia.org:")
    # ---
    page = wiki_MainPage(title_file, "commons", family="wikimedia")
    # ---
    if not page.exists() :
        printe.output(f"<<lightred>>{title} not exists on commons.wikimedia.org")
        return False
    # ---
    if page.isRedirect() :
        title_file = page.get_redirect_target()
        page = wiki_MainPage(title_file, "commons", family="wikimedia")
    # ---
    file_text = page.get_text()
    file_text = file_text.replace("{{PD-user|norro}}", "")

    api_commons = wiki_NEW_API("commons", family="wikimedia")
    img_url = api_commons.Get_image_url(title_file)
    # ---
    summary = "Bot: import from commons.wikimedia.org"
    # ---
    # upload = upload_file.upload_by_url(title, file_text, img_url, comment=summary, code="www", family="nccommons")
    upload = api.upload_by_url(title, file_text, img_url, comment=summary)
    # ---
    return upload


def get_wanted_images():
    pages = api_new.querypage_list(qppage="Wantedfiles", qplimit="100", Max=100)
    # "results": [ { "value": "32", "ns": 6, "title": "File:Pictogram voting info.svg" }, {}, ... ]

    if pages:
        pages = [x["title"] for x in pages]

    return pages


def start():
    # images = get_wanted_images()
    images = imges_liist
    # ---
    check_titles = api_new.Find_pages_exists_or_not(images)
    # ---
    missing_images = [ x for x in images if not check_titles.get(x, False) ]
    # ---
    printe.output(f"<<yellow>> wanted images: {len(images)}, missing_images: {len(missing_images)}")
    # ---
    for n, image in enumerate(missing_images, 1):
        printe.output(f"<<yellow>> file: {n}/{len(missing_images)} - {image}")
        import_file(image)


if __name__ == "__main__":
    start()
