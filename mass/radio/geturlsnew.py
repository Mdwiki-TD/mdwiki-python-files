"""

python3 core8/pwb.py mass/radio/geturlsnew

"""

import requests
from bs4 import BeautifulSoup
from newapi import printe

# ---
from mass.radio.jsons_files import dump_json_file, jsons

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0, systems=0)
# ---
systems = [
    "Breast",
    "Cardiac",
    "Central Nervous System",
    "Chest",
    "Forensic",
    "Gastrointestinal",
    "Gynaecology",
    "Haematology",
    "Head & Neck",
    "Hepatobiliary",
    "Interventional",
    "Musculoskeletal",
    "Obstetrics",
    "Oncology",
    "Paediatrics",
    "Spine",
    "Trauma",
    "Urogenital",
    "Vascular",
    "Not Applicable",
]  # 50  # 69  # 549  # 344  # 16  # 356  # 110  # 23  # 272  # 139  # 30  # 814  # 45  # 208  # 303  # 127  # 171  # 221  # 180  # 7
# ---
lenth_of_systems = {
    "Breast": 50,
    "Cardiac": 69,
    "Central Nervous System": 549,
    "Chest": 344,
    "Forensic": 16,
    "Gastrointestinal": 356,
    "Gynaecology": 110,
    "Haematology": 23,
    "Head & Neck": 272,
    "Hepatobiliary": 139,
    "Interventional": 30,
    "Musculoskeletal": 814,
    "Obstetrics": 45,
    "Oncology": 208,
    "Paediatrics": 303,
    "Spine": 127,
    "Trauma": 171,
    "Urogenital": 221,
    "Vascular": 180,
    "Not Applicable": 7,
}


# ---
def get_urls_system(system, only_one=False, return_tab=False, len_all=0):
    print(f"get_urls system:{system}::")
    # ---
    sys2 = system
    # ---
    if sys2 == "Head & Neck":
        sys2 = "Head+%26+Neck"
    # ---
    sys2 = sys2.replace(" ", "+")
    # ---
    # url = f'https://radiopaedia.org/search?lang=us&page=1&scope=cases&sort=title&system={sys2}'
    # url = f'https://radiopaedia.org/search?lang=us&page=1&scope=cases&sort=date_of_publication&system={sys2}'
    url = f"https://radiopaedia.org/search?lang=us&page=1&scope=cases&sort=completeness&system={sys2}"
    # ---
    tat = {}
    # ---
    n = 0
    # ---
    while url:
        n += 1
        print(f"get url: {url}")
        response = requests.get(url, timeout=10)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Step 2: Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            # find  <a class="next_page" aria-label="Next page" rel="next" href="/search?lang=us&amp;page=2&amp;scope=cases&amp;sort=title&amp;system=Spine">Next &#8594;</a>
            next_page = soup.find("a", class_="next_page")
            if next_page:
                url = "https://radiopaedia.org" + next_page.get("href").strip()
            else:
                url = None
            # ---
            if n == 1 and only_one:
                # find len of search results
                # <div role="navigation" aria-label="Pagination" class="pagination clear">
                pagination = soup.find("div", role="navigation", class_="pagination clear")
                # ---
                last_href = 0
                # ---
                if pagination:
                    # get the link before the last one
                    last_href = pagination.find_all("a")
                    if len(last_href) > 2:
                        last_href = last_href[-2].text.strip()
                # ---
                print(f"last_href: {last_href}")
                return last_href
            # ---
            links = soup.find_all("a", class_="search-result search-result-case")
            # ---
            for link in links:
                # ---
                href = link.get("href").strip()
                href = href.replace("?lang=us", "")
                href = f"https://radiopaedia.org{href}"
                # ---
                title = link.find("h4", class_="search-result-title-text").text.strip()
                # ---
                author = ""
                # <div class="search-result-author"><span>Henry Knipe</span></div>
                au = link.find("div", class_="search-result-author")
                if au:
                    author = au.text.strip() or ""
                # ---
                # <span class="published">Published 15 Oct 2015</span>
                published = link.find("span", class_="published").text.replace("Published ", "").strip()
                # ---
                tab = {
                    "title": title,
                    "system": system,
                    "author": author,
                    "published": published,
                    "url": href,
                }
                # ---
                jsons.infos[href] = tab
                # ---
                if return_tab:
                    tat[href] = tab
                else:
                    tat[href] = title
        # ---
        print(f"n:{n}, lenth of links: {len(links)}, tat: {len(tat)}/{len_all}")
    # ---
    print(f"lenth of tat: {len(tat)}")

    return tat


def main():
    # ---
    jsons.systems.update({x: False for x in systems if x not in jsons.systems})
    # ---
    for numb, system in enumerate(systems, start=1):
        # ---
        if jsons.systems[system]:
            printe.output(f"<<green>> system:{system} already in jsons.systems. Skipping.")
            continue
        # ---
        urls_data = get_urls_system(system)
        # ---
        if not urls_data:
            continue
        # ---
        new = {x: v for x, v in urls_data.items() if x not in jsons.urls}
        # ---
        print(f"new: {len(new)}, urls_data: {len(urls_data)}")
        # ---
        if new:
            jsons.urls.update(new)
        # ---
        dump_json_file("jsons/urls.json", jsons.urls, False)
        dump_json_file("jsons/infos.json", jsons.infos, False)
        # ---
        jsons.systems[system] = True
        # dump
        dump_json_file("jsons/systems.json", jsons.systems, False)
    # ---
    dump_json_file("jsons/urls.json", jsons.urls, False)
    dump_json_file("jsons/infos.json", jsons.infos, False)
    # ---


if __name__ == "__main__":
    main()
