'''

1. open url https://openpress.usask.ca/undergradimaging/
2. match all <p class="toc__title">
like:(
    <p class="toc__title"><a href="https://openpress.usask.ca/undergradimaging/chapter/radiation-in-medical-imaging/">Radiation in Medical Imaging: The x-ray Tube</a></p>)
    
3. get href and title
4. add title to dict urls contains: {title: {"url": href, "images": {}}}
5. save urls to json file named urls.json


python3 I:/mdwiki/pybot/mass/usask/geturls.py
python3 core8/pwb.py mass/usask/geturls
'''
import requests
from bs4 import BeautifulSoup
import os
import json
import sys
from pathlib import Path

Dir = Path(__file__).parent
urlsfile = os.path.join(str(Dir), 'urls.json')

url = "https://openpress.usask.ca/undergradimaging/"

# Step 1: Open the URL
print(f"Step 1: Open URL: {url}")

response = requests.get(url)
print(f"Step 1: Opened the URL. Status Code: {response.status_code}")

# Check if the request was successful (status code 200)
if response.status_code != 200:
    print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
    sys.exit()

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
print("Step 2: Parsed the HTML content.")

# Step 3 and 4: Extract href and title, and add to the dictionary
urls_dict = {}
for p_tag in soup.find_all('p', class_='toc__title'):
    a_tag = p_tag.find('a')
    if a_tag:
        title = a_tag.text.strip()
        href = a_tag['href']
        urls_dict[title] = {"url": href, "images": {}}
        print(f"Step 3-4: Extracted href and title - Title: {title}, Href: {href}")

print(f"lenth of urls_dict: {len(urls_dict)}")

# Step 5: Save the dictionary to a JSON file
with open(urlsfile, 'w') as json_file:
    json.dump(urls_dict, json_file, indent=2)
print("Step 5: Saved the dictionary to 'urls.json'.")
