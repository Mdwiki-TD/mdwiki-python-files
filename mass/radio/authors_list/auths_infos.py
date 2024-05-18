'''
"""This module contains functions for retrieving author information from Radiopaedia."""

from mass.radio.authors_list.auths_infos import get_author_infos

'''
import requests
import sys
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
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return
    # ---
    return soup


def get_user_infos(url):
    """Retrieve user information from a given URL."""
    """Parameters:
        - url: The URL to retrieve the user information from."""
    """Return:
        - user_info: A dictionary containing the user's URL and location."""
    # ---
    user_info = {
        "url": "",
        "location": "",
        "cases": 0
    }
    # ---
    if "empty" in sys.argv:
        return user_info
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
        a = div.find("a")
        if a:
            user_url = a.get('href')
            if user_url and user_url.startswith("/"):
                user_url = f"https://radiopaedia.org{user_url}"
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
    """Retrieve author information for a given author and first case URL."""
    """Parameters:
        - auth: The author's ID.
        - first_case_url: The URL of the first case contributed by the author."""
    """Return:
        - info: A dictionary containing the author's URL and location."""
    # ---
    printe.output(f"<<yellow>> get_author_infos:{auth=}, {first_case_url=}")
    # ---
    info = {
        "url": "",
        "location": "",
        "cases": 0
    }
    # ---
    na = get_user_infos(first_case_url)
    # ---
    return na
