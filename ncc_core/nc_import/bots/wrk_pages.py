
import wikitextparser as wtp
from newapi.wiki_page import MainPage
'''
page      = MainPage(title, 'ar', family='wikipedia')
exists    = page.exists()
text      = page.get_text()
timestamp = page.get_timestamp()
user      = page.get_user()
links     = page.page_links()
words     = page.get_words()
purge     = page.purge()
templates = page.get_templates()
save_page = page.save(newtext='', summary='', nocreate=1, minor='')
create    = page.Create(text='', summary='')
'''

def work_one_temp(temp, code):
    args = temp.arguments
    # ---
    print(args)
    # ---

def work_on_temps(text, temps):
    new_text = text
    # ---
    for temp in temps:
        string = temp.string
        # ---
        # {{NC|file name from NC Commons|caption}}
        temp_new_text = work_one_temp(temp, code)
        # ---
        if temp_new_text != string:
            new_text = new_text.replace(string, temp_new_text)
    # ---
    return new_text

def work_on_pages(code, pages):

    for numb, page in enumerate(pages, 1):
        print(f"{numb}: {page}:")
        # ---
        page      = MainPage(page, code, family='wikipedia')
        if not page.exists():
            print(f"page {page} not exists!")
            continue
        # ---
        text = page.get_text()
        parsed = wtp.parse(text)
        # ---
        temps = []
        # ---
        for temp in parsed.templates:
            # ---
            name = str(temp.normal_name()).strip().lower().replace('_', ' ')
            if name == 'NC':
                temps.append(temp)
        # ---
        new_text = work_on_temps(page, temps)
        # ---
        if new_text != text:
            page.save(newtext=new_text, summary="bot: fix NC")
