'''

python3 core8/pwb.py mass/radio/get_ids

'''
import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json

main_dir = Path(__file__).parent
to_work_f = os.path.join(str(main_dir), 'jsons/to_work.json')

ids_file = os.path.join(str(main_dir), 'jsons/ids.json')

if not os.path.exists(ids_file):
    with open(ids_file, 'w', encoding='utf-8') as f:
        f.write("{}")

def get_ids(url):
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
    # <a class="view-fullscreen-link" href="/cases/97085/studies/117071?lang=us">
    studies_ = soup.find_all('a', class_='view-fullscreen-link')
    for link in studies_:
        #---
        href = link.get('href').strip()
        href = href.replace('?lang=us', '')
        href = f'https://radiopaedia.org{href}'
        #---
        studies.append(href)
    #---
    hidden_data_divs = soup.find_all('div', class_='hidden data')
    # ---
    case_id = ''
    # ---
    if hidden_data_divs:
        for index, hidden_data_div in enumerate(hidden_data_divs, start=1):
            # Extract JSON content from the div
            json_content = hidden_data_div.text
            if json_content.find('caseId') != -1:
                # Parse JSON to get caseId
                try:
                    case_id = int(json_content.split('"caseId":')[1].split(',')[0])
                    break
                except (ValueError, IndexError):
                    print("Error: Unable to extract caseId from JSON.")

    print(f"case_id: {case_id}, studies: {str(studies)}")
    return case_id, studies

def main():
    ids = {}

    with open(to_work_f, 'r', encoding='utf-8') as f:
        to_work = json.loads(f.read())
    print(f"lenth of to_work: {len(to_work)}")

    with open(ids_file, 'r', encoding='utf-8') as f:
        ids = json.loads(f.read())

    n = 0
    for url, title in to_work.items():
        n += 1
        #---
        print(f"n: {n}")
        #---
        in_ids  = ids.get(url, {}).get("caseId", '')
        in_case = ids.get(url, {}).get("studies", [])
        #---
        if in_ids and in_case:
            continue
        #---
        case_id, studies = get_ids(url)
        ids[str(case_id)] = {"url":url, "caseId": case_id, "title": title, "studies": studies}
        #---
        if n % 100 == 0:
            with open(ids_file, 'w', encoding='utf-8') as f:
                json.dump(ids, f, ensure_ascii=False, indent=4)
        #---
    
    print("Step 5: Saved the dictionary to 'jsons/ids.json'.")
    # Step 5: Save the dictionary to a JSON file
    with open(ids_file, 'w', encoding='utf-8') as f:
        json.dump(ids, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
