from newapi.wiki_page import NEW_API


def get_pages(code):
    """
    Retrieves template pages related to a given language code.
    """
    api_new = NEW_API(code, family="wikipedia")

    api_new.Login_to_wiki()

    pages = api_new.Get_template_pages("Template:NC", namespace="*", Max=10000)

    return pages
