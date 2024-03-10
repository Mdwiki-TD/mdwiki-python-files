

from newapi.wiki_page import MainPage
from newapi import printe
'''
page      = MainPage(title, 'ar', family='wikipedia')
exists    = page.exists()
text      = page.get_text()
save_page = page.save(newtext='', summary='', nocreate=1, minor='')
'''

def import_file(title, code):
    printe.output(f"<<yellow>>import_file: File:{title} to {code}wiki:")
    