"""

python3 core8/pwb.py nc_import/bot

"""
from nc_import.bots.gt_pages import get_pages
from nc_import.bots.wrk_pages import work_on_pages

langs = [
    # "af",
    "ar"
]

def start():
    for code in langs:
        pages = get_pages(code)
        work_on_pages(code, pages)

if __name__ == '__main__':
    start()