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
urlsfile = os.path.join(str(main_dir), 'jsons/urls.json')

if not os.path.exists(urlsfile):
    with open(urlsfile, 'w', encoding='utf-8') as f:
        f.write("{}")

with open(urlsfile, 'r', encoding='utf-8') as f:
    all_urls = json.loads(f.read())
print(f"lenth of all_urls: {len(all_urls)}")

def get_urls(page_num):
    print(f"get_urls {page_num}::")

    url = f'https://radiopaedia.org/search?lang=us&page={page_num}&scope=cases&sort=title'
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return None

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='search-result search-result-case')

    tat = {}
    for link in links:
        #---
        href = link.get('href').strip()
        href = href.replace('?lang=us', '')
        href = f'https://radiopaedia.org{href}'
        #---
        title = link.find('h4', class_='search-result-title-text').text.strip()

        # print(f"Step 3-4: Href[{href}] = '{title}'")

        tat[href] = title
    #---
    print(f"lenth of tat: {len(tat)}")

    return tat

def main():
    all_urls = {}

    with open(urlsfile, 'r', encoding='utf-8') as f:
        all_urls = json.loads(f.read())

    for page_num in range(1, 2841):
        urls_data = get_urls(page_num)
        if urls_data:
            all_urls.update(urls_data)

        
        if page_num % 100 == 0:
            # Step 5: Save the dictionary to a JSON file
            with open(urlsfile, 'w', encoding='utf-8') as f:
                json.dump(all_urls, f, ensure_ascii=False, indent=4)

    # Step 5: Save the dictionary to a JSON file
    with open(urlsfile, 'w', encoding='utf-8') as f:
        json.dump(all_urls, f, ensure_ascii=False, indent=4)

    print("Step 5: Saved the dictionary to 'jsons/urls.json'.")

if __name__ == "__main__":
    main()
