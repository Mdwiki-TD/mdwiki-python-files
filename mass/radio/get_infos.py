'''

python3 core8/pwb.py mass/radio/get_infos

'''
import time
import requests
from bs4 import BeautifulSoup
# ---
from mass.radio.jsons_files import jsons, dump_json_file, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)

def get_id_infos(url):
    # ---
    case_tab = {"url": url, "caseId": "", "title": "", "studies": [], "system": "", "author": "", "published": ""}
    # ---
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return case_tab
    # ---
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return case_tab
    # ---
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # ---
    # <a class="view-fullscreen-link" href="/cases/97085/studies/117071?lang=us">
    studies_ = soup.find_all('a', class_='view-fullscreen-link')
    # ---
    studies = []
    for link in studies_:
        # ---
        href = link.get('href').strip()
        href = href.replace('?lang=us', '')
        href = f'https://radiopaedia.org{href}'
        # ---
        studies.append(href)
    # ---
    hidden_data_divs = soup.find_all('div', class_='hidden data')
    # ---
    case_id = ''
    # ---
    if hidden_data_divs:
        for _, hidden_data_div in enumerate(hidden_data_divs, start=1):
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
    # ---
    title = ''
    # ---
    # <div class='case-link'><a class="link-on-dark" href="/cases/cervical-rib-21?lang=us">Cervical rib</a></div>
    case_link = soup.find('div', class_='case-link')
    if case_link:
        title = case_link.find('a', class_='link-on-dark').text.strip()
    # ---
    author = ''
    # <meta name="author" content="Frank Gaillard"/>
    au = soup.find('meta', attrs={'name': 'author'})
    if au:
        author = au.get('content') or ''
    # ---
    case_tab['caseId']  = case_id
    case_tab['studies'] = studies
    case_tab['title']   = title
    case_tab['author']  = author
    # ---
    return case_tab


def mainnew():
    # ---
    urls_to_get_info = jsons.urls_to_get_info
    # ---
    print(f"lenth of urls_to_get_info: {len(urls_to_get_info)}")
    # ---
    for n, url in enumerate(urls_to_get_info, start=1):
        # ---
        print(f"n: {n}/{len(urls_to_get_info)}: {url}")
        # ---
        case_tab = get_id_infos(url)
        # ---
        case_id = case_tab['caseId']
        # ---
        jsons.all_ids[str(case_id)] = case_tab
        # ---
        if n % 100 == 0:
            # dumps_jsons(all_ids=1)
            dump_json_file('jsons/all_ids.json', jsons.all_ids, False)
    # ---
    print("Step 5: Saved all_ids dictionary to jsons.")

    # Step 5: Save the dictionary to a JSON file
    # dumps_jsons(all_ids=1)
    dump_json_file('jsons/all_ids.json', jsons.all_ids, False)


if __name__ == "__main__":
    mainnew()
