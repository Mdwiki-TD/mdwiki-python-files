# -*- coding: utf-8 -*-
"""
Usage:
from mass.eyerounds.bots.get_case_info import extract_infos_from_url

:write python code to do:
* open url: https://eyerounds.org/cases/254-anterior-chamber-cilium.htm
* get div <div class="col-md-12 mt-4 text-left">
* get authors and date from h5 code like:
<div>
    <h5 class=" mt-4"> Zachary Mayo, BS; <a href="../bio/authors/Stiff-Heather.htm">Heather A. Stiff, MD</a>; <a href="../bio/authors/Parekh-Prashant.htm">Prashant K. Parekh, MD, MBA</a>; <a href="../bio/authors/Haugsdal-Jaclyn.htm">Jaclyn M. Haugsdal, MD</a>; <a href="../bio/authors/Oetting-Thomas.htm">Thomas A. Oetting, MD, MS</a> </h5>
    <h5 class=" mt-2 text-muted"> posted July 5, 2017 </h5>
</div>
*. add date and authors to dict {"date": "", "authors": []}
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from newapi import printe

def extract_images_from_tag(soup):

    # match all <table width="100%" class="figure">
    # figure_tags = soup.find_all("table", class_="figure")

    images_info = {}
    urls = soup.find_all("a")
    
    # filter only urls with /cases-i/
    new_urls = [url for url in urls if url.get('href') and url.get('href').find("/cases-i/") != -1]

    printe.output(f'new_urls: {len(new_urls)=}, urls: {len(urls)}')
    # Iterate over each 'figure' tag

    for n, url in enumerate(new_urls, 1):
        printe.output(f'<<purple>> >> url {n}/{len(new_urls)}')
        printe.output(f'\t<<yellow>>{url}')
        # <a href="../cases-i/case254/Fig1-LRG.jpg"><img alt="Figure 1: Slit lamp photograph showing 6mm cilium with overlying pigment on the iris at 6 o'clock just nasal to an area of iris atrophy. The cilium extends towards the pupil." class="figure" src="../cases-i/case254/Fig1.jpg" width="100%"/></a>

        img_url = url.get('href')
        
        img_alt = ""

        img_tag = url.find('img')
        if img_tag:
            img_alt = img_tag.get('alt', '')
            img_alt = re.sub(r'\(please see: .*?\)', '', img_alt)
            
        printe.output(f'\t\t <<yellow>> img_url: {img_url}')

        if img_url:
            if img_url.startswith('../cases-i/'):
                img_url = 'https://eyerounds.org/cases-i/' + img_url.replace('../cases-i/', '')
            images_info[img_url.strip()] = img_alt.strip()

    return images_info

def fix_auth(x):
    x = x.replace("\n", "")
    x = re.sub(r'\s+', ' ', x)
    x = x.strip()
    return x
    
def extract_infos_from_url(url):
    # Print the URL being processed
    printe.output(f"\t Processing URL: {url}")

    # Send a GET request to the URL and get the response
    response = requests.get(url)

    # Check if the response status code is 200 (OK)
    if response.status_code != 200:
        # Print an error message if the request failed
        printe.output(f"\t\t Failed to fetch content from {url}")

        # Return an empty dictionary
        return {}

    data = {}
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific div
    div = soup.find("div", class_="col-md-12 mt-4 text-left")

    # Find the h5 tags inside the div
    author_h5 = div.find("h5", class_="mt-4")

    authors = { fix_auth(a.text) : a.get("href") or "" for a in author_h5.find_all("a") }

    # Extract authors
    author_h5_text = author_h5.text.strip("\n")
    author_h5_text = re.sub(r'\s+', ' ', author_h5_text)

    if author_h5_text.find(";") != -1:
        auths_text = [ x.strip() for x in author_h5_text.split(";")]
    else:
        u = author_h5_text
        # ---
        for au in authors:
            if au in u:
                u = u.replace(au, "")
        # ---
        u = re.sub(r"[\s,]+$", "", u)
        # ---
        auths_text = [ u.strip() ]
    
    for x in auths_text:
        if x not in authors:
            authors[x] = ""
    
    # add https://eyerounds.org/bio/ to authors links
    for k, v in authors.copy().items():
        if v and v.startswith("../bio/"):
            authors[k] = "https://eyerounds.org/bio/" + v.replace("../bio/", "")

    # Combine authors and date into a dictionary
    data["authors"] = authors

    # Extract date
    # <h5 class=" mt-2 text-muted"> posted July 5, 2017 </h5>
    date_h5 = div.find("h5", class_="mt-2 text-muted")
    data["date"] = date_h5.text.strip()

    
    images_info = extract_images_from_tag(soup)

    # Return the dictionary containing the image URLs and captions
    data["images"] = images_info
    # ---
    return data

if __name__ == '__main__':
    # python3 core8/pwb.py mass/eyerounds/bots/get_case_info
    url = "https://eyerounds.org/cases/239-post-vit-cataract-surgery.htm"
    data = extract_infos_from_url(url)
    printe.output(json.dumps(data, indent=4))