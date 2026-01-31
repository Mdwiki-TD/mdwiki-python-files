#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/bot ask

tfj run copyen --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_to_en/bot"

"""
from apis import cat_cach, mdwiki_api
from copy_to_en.bots import text_changes  # text = text_changes.work(text)
from copy_to_en.bots.ref import fix_ref  # text = fix_ref(first, alltext)
from newapi.wiki_page import MainPage


def main():
    # ---
    all_pages = cat_cach.from_cache()
    # ---
    for n, x in enumerate(all_pages):
        print(f"{n}/{len(all_pages)} : {x}")
        # ---
        alltext = mdwiki_api.GetPageText(x)
        # ---
        if not alltext:
            print("no text: " + x)
            continue
        # ---
        first = alltext.split("==")[0].strip()
        # ---
        first = first + "\n\n==References==\n<references />"
        newtext = first
        # ---
        newtext = fix_ref(first, alltext)
        # ---
        newtext = text_changes.work(newtext)
        # ---
        new_title = "User:Mr. Ibrahem/" + x
        # ---
        page = MainPage(new_title, "simple")
        # ---
        summary = "from https://mdwiki.org/wiki/" + x.replace(" ", "_")
        # ---
        if page.exists():
            _p_t = page.get_text()
            # ---
            page.save(newtext, summary=summary, nocreate=0)
        else:
            print("page not found: " + new_title)
            page.Create(text=newtext, summary=summary)


if __name__ == "__main__":
    main()
