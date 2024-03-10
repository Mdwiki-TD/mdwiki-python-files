from newapi.wiki_page import MainPage, NEW_API

# api_new = NEW_API('en', family='wikipedia')
# login    = api_new.Login_to_wiki()
# pages  = api_new.Get_template_pages(title, namespace="*", Max=10000)
"""
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
"""


def get_pages(code):
    api_new = NEW_API(code, family="wikipedia")

    api_new.Login_to_wiki()

    pages = api_new.Get_template_pages("Template:NC", namespace="*", Max=10000)

    return pages
