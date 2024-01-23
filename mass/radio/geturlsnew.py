'''

write python code to do:

main_dir = Path(__file__).parent
urlsfile = os.path.join(str(main_dir), 'jsons/urls.json')

1. open urls  https://radiopaedia.org/search?lang=us&page=1&scope=cases&sort=title start at page 1 to 2840
2. match all <a class="search-result search-result-case" href="*">
like:(
    <a class="search-result search-result-case" href="/cases/11-pair-ribs?lang=us">
        <h4 class="search-result-title-text">13 pairs of ribs and absent radius</h4>
    </a>
)
    
3. add title and href to dict urls
5. save urls to json file named urls.json


python3 core8/pwb.py mass/radio/geturls

'''
import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json

main_dir = Path(__file__).parent

files = {
    "urls": os.path.join(str(main_dir), 'jsons/urls.json'),
    "infos": os.path.join(str(main_dir), 'jsons/infos.json'),
}

jsons = {}

for k, v in files.items():
    if not os.path.exists(v):
        with open(v, 'w', encoding='utf-8') as f:
            f.write("{}")
    with open(v, 'r', encoding='utf-8') as f:
        jsons[k] = json.loads(f.read())

print(f"lenth of jsons['urls']: {len(jsons['urls'])}")


def get_urls_system(system):
    print(f"get_urls system:{system}::")

    url = f'https://radiopaedia.org/search?lang=us&page=1&scope=cases&sort=title&system={system}'
    # ---
    tat = {}
    # ---
    while url:
        print(f"get url: {url}")
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
            return None

        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # find  <a class="next_page" aria-label="Next page" rel="next" href="/search?lang=us&amp;page=2&amp;scope=cases&amp;sort=title&amp;system=Spine">Next &#8594;</a>
        next_page = soup.find('a', class_='next_page')
        if next_page:
            url = "https://radiopaedia.org" + next_page.get('href').strip()
        else:
            url = None
        links = soup.find_all('a', class_='search-result search-result-case')

        print(f"lenth of links: {len(links)}, tat: {len(tat)}")
        for link in links:
            # ---
            href = link.get('href').strip()
            href = href.replace('?lang=us', '')
            href = f'https://radiopaedia.org{href}'
            # ---
            title = link.find('h4', class_='search-result-title-text').text.strip()
            # ---
            # <div class="search-result-author"><span>Henry Knipe</span></div>
            author = link.find('div', class_='search-result-author').text.strip()
            # ---
            # <span class="published">Published 15 Oct 2015</span>
            published = link.find('span', class_='published').text.replace('Published ', '').strip()
            # ---
            jsons['infos'][href] = {
                "title": title,
                "system": system,
                "author": author,
                "published": published,
                "url": href
            }
            tat[href] = title
    # ---
    print(f"lenth of tat: {len(tat)}")

    return tat

def dumps_jsons():

    for k, v in files.items():
        with open(v, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsons[k], ensure_ascii=False, indent=4))
            print(f"Step 5: Saved the dictionary to '{v}'.")

def main():
    # ---
    with open(files['urls'], 'r', encoding='utf-8') as f:
        jsons['urls'] = json.loads(f.read())
    # ---
    systems = [
        "Breast",
        "Cardiac",
        "Central Nervous System",
        "Chest",
        "Forensic",
        "Gastrointestinal",
        "Gynecology",
        "Hematology",
        "Head & Neck",
        "Hepatobiliary",
        "Interventional",
        "Musculoskeletal",
        "Obstetrics",
        "Oncology",
        "Pediatrics",
        "Spine",
        "Trauma",
        "Urogenital",
        "Vascular",
        "Not Applicable"
    ]
    # ---
    for system in systems:
        for page_num in range(200, 400):
            urls_data = get_urls_system(system)
            # ---
            new = {x:v for x, v in urls_data.items() if x not in jsons['urls']}
            # ---
            print(f"new: {len(new)}, urls_data: {len(urls_data)}")
            # ---
            if new:
                jsons['urls'].update(new)
            # ---
            if page_num % 100 == 0:
                dumps_jsons()
    # ---
    dumps_jsons()

if __name__ == "__main__":
    main()
