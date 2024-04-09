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
    "File:Pictogram voting info.svg",
    "File:Symbol redirect vote.svg",
    "File:BA candidate.svg",
    "File:GA candidate.svg",
    "File:Pictogram-voting-question.svg",
    "File:Pictogram voting comment.svg",
    "File:Pictogram voting delete.svg",
    "File:Pictogram voting question-blue.svg",
    "File:Symbol abstain vote.svg",
    "File:Symbol delete vote.svg",
    "File:Symbol keep vote.svg",
    "File:Symbol neutral vote.svg",
    "File:Symbol oppose vote.svg",
    "File:Symbol oppose vote oversat.svg",
    "File:Symbol speedy delete vote.svg",
    "File:Symbol speedy keep.svg",
    "File:Symbol strong support vote.svg",
    "File:Symbol support vote.svg",
    "File:Symbol unsupport vote.svg",
    "File:Thumbs-up-icon.svg",
    "File:Time2wait.svg",
    "File:X mark.svg",
    "File:Yellow check.svg",
    "File:Arrow facing left - Green.svg",
    "File:Cc-zero.svg",
    "File:Cc.logo.circle.svg",
    "File:Cc-by new.svg",
    "File:Cc-nc.svg",
    "File:Cc-nd.svg",
    "File:Cc-nd white.svg",
    "File:Cc-sa.svg",
    "File:Dialog-warning.svg",
    "File:Magenband 52jw - CT Volumen Rendering - 001.jpg",
    "File:Magenband 52jw - CT Volumen Rendering - 002.jpg",
    "File:Magenband 52jw - CT Volumen Rendering - 003.jpg",
    "File:Magenband 52jw - CT Volumen Rendering - 004.jpg",
    "File:Redirect arrow without text.svg",
    "File:4 icon.svg",
    "File:CC BY.png",
    "File:CC NC.png",
    "File:CC ND.png",
    "File:CC SA.png",
    "File:Cc-by.svg",
    "File:Cc-by white.svg",
    "File:Circle-ye-5.svg",
    "File:Commonist2.svg",
    "File:Commons-emblem-issue.svg",
    "File:Crystal Clear app gimp",
    "File:Example.jpg",
    "File:Gnome-x-office-drawing.svg",
    "File:Green copyright.svg",
    "File:Heptagon.svg",
    "File:Icono de traducción.svg",
    "File:Inkscape-small.svg",
    "File:Invalid SVG 1.1",
    "File:LA2-NSRW-1-0007.jpg",
    "File:Nr02 blue.svg",
    "File:Nr03 red.svg",
    "File:OOjs UI icon alert-yellow.svg",
    "File:One.svg",
    "File:Query-road.png",
    "File:SVG Simple Icon.svg",
    "File:SVG example7.svg",
    "File:Trademark Warning Symbol.svg",
    "File:W3C red.svg",
]

def import_file(title):
    """
    Imports a file from Wikimedia Commons to NC Commons.
    """
    printe.output(f"<<yellow>>import_file: File:{title} to nccommons:")
    # ---
    title_file = f"File:{title}" if not title.startswith("File:") else title
    printe.output(f"<<yellow>>get_file_text: {title} from commons.wikimedia.org:")

    page = wiki_MainPage(title_file, "commons", family="wikimedia")
    file_text = page.get_text()
    file_text = file_text.replaces("{{PD-user|norro}}", "")

    api_commons = wiki_NEW_API("commons", family="wikimedia")
    img_url = api_commons.Get_image_url(title_file)
    # ---
    summary = "Bot: import from commons.wikimedia.org"
    # ---
    # upload = upload_file.upload_by_url(title, file_text, img_url, comment=summary, code="www", family="nccommons")
    upload = upload = api.upload_by_url(title, file_text, img_url, comment=summary)
    # ---
    return upload


def get_wanted_images():
    pages = api_new.querypage_list(qppage="Wantedfiles", qplimit="100", Max=100)
    # "results": [ { "value": "32", "ns": 6, "title": "File:Pictogram voting info.svg" }, {}, ... ]

    if pages:
        pages = [x["title"] for x in pages]

    if not pages:
        pages = imges_liist

    return pages


def start():
    images = get_wanted_images()
    check_titles = api_new.Find_pages_exists_or_not(images)
    # ---
    missing_images = [ x for x in images if x not in check_titles ]
    # ---
    printe.output(f"<<yellow>> wanted images: {len(images)}, missing_images: {len(missing_images)}")
    # ---
    for n, image in enumerate(missing_images, 1):
        printe.output(f"<<yellow>> file: {n}/{len(images)} - {image}")
        import_file(image)


if __name__ == "__main__":
    start()
