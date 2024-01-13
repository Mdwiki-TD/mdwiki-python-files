'''

python3 core8/pwb.py mass/radio/authors

'''
import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json

main_dir = Path(__file__).parent

authors_file = os.path.join(str(main_dir), 'jsons/authors.json')

if not os.path.exists(authors_file):
    with open(authors_file, 'w', encoding='utf-8') as f:
        f.write("{}")

ids_file = os.path.join(str(main_dir), 'jsons/ids.json')
with open(ids_file, 'r', encoding='utf-8') as f:
    ids = json.loads(f.read())

def get_author(url):
    studies = []
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return '', studies

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return '', studies

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('meta', attrs={'name': 'author'}).get('content')

def main():
    n = 0
        
    with open(authors_file, 'r', encoding='utf-8') as ff:
        authors = json.loads(ff.read())

    for url, tab in ids.items():
        caseId = str(tab['caseId'])
        n += 1
        #---
        print(f"n: {n}/ {len(ids)}")
        #---
        if caseId in authors:
            continue
        #---
        author = get_author(url)
        print(f"caseId:{caseId}, Author: {author}")
        #---
        authors[caseId] = author
        #---
        if n % 50 == 0:
            with open(authors_file, 'w', encoding='utf-8') as f:
                json.dump(authors, f, ensure_ascii=False, indent=4)
        #---
    
    print("Step 5: Saved the dictionary to 'jsons/authors.json'.")

    # Step 5: Save the dictionary to a JSON file
    with open(authors_file, 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
