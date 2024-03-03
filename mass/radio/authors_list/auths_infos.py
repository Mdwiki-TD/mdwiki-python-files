'''

from mass.radio.authors_list.auths_infos import get_author_infos

'''
import re
import requests
import sys
import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
from newapi import printe

def get_soup(url):
    # ---
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    # ---
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return
    # ---
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # ---
    return soup
def get_user_infos(url):
    # ---
    user_info = {"url": "", "location": ""}
    # ---
    location = ""
    # ---
    soup = get_soup(url)
    # ---
    if not soup:
        return user_info
    # ---
    # <div class="author-info">Case contributed by <a href="/users/frank?lang=us">Frank Gaillard</a>        </div>
    user_url = ""
    div = soup.find('div', class_='author-info')
    if div:
        a = div.find('a')
        if a:
            user_url = a.get('href')
            if user_url and user_url.startswith("/"):
                user_url = "https://radiopaedia.org" + user_url
    # ---
    if user_url:
        soup2 = get_soup(user_url)
        if soup2:
            # <dd class="institution-and-location">Melbourne, Australia</dd>
            dd = soup2.find('dd', class_='institution-and-location')
            if dd:
                location = dd.text.strip()
    # ---
    user_info["location"] = location
    user_info["url"] = user_url
    # ---
    printe.output(f" {location=}, {user_url=}")
    # ---
    return user_info

def get_author_infos(auth, first_case_url):
    # ---
    printe.output(f"<<yellow>> get_author_infos:{auth=}, {first_case_url=}")
    # ---
    info = {
        "url" : "",
        "location" : ""
    }
    # ---
    na = get_user_infos(first_case_url)
    # ---
    return na
