"""

python3 core8/pwb.py nc_import/views
fetch("https://pageviews.wmcloud.org/pageviews/api.php?pages=Kat%7CHond&project=af.wikipedia.org&start=2015-07-01&end=2024-03-27&totals=true", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7,sk;q=0.6,zh-CN;q=0.5,zh-TW;q=0.4,zh;q=0.3",
    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://pageviews.wmcloud.org/pageviews/?project=af.wikipedia.org&platform=all-access&agent=user&redirects=0&range=all-time&pages=Kat|Hond",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
});
"""
from nc_import.bots.get_langs import get_langs_codes

def get_views(code):
    endpoint = "https://pageviews.wmcloud.org/massviews/api.php"
    category = "Category:Files_imported_from_NC_Commons"
    # ---
    # https://pageviews.wmcloud.org/massviews/api.php?project=af.wikipedia.org&category=Files_imported_from_NC_Commons&limit=20000
    # ---
    params = {
        "project": f"{code}.wikipedia.org",
        "category": category
    }
    # ---
    # result example: [{"title":"Chondrosarcoma_of_the_nasal_septum_(Radiopaedia_165701-135935_Sagittal_2).jpeg","ns":6}]
    # ---
    

def start():
    """
    A function that starts the process by iterating over languages, getting pages for each language, and then working on those pages.
    """
    langs = get_langs_codes()
    # ---
    for code in langs:
        pages = get_views(code)


if __name__ == "__main__":
    start()
