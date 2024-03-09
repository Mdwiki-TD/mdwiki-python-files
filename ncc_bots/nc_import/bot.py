
from ncc_import import get_pages

langs = [
    "af",
    "ar"
]

def start():
    for code in langs:
        pages = get_pages(code)
        

if __name__ == '__main__':
    start()