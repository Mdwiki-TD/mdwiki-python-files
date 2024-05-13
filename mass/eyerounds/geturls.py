"""

python3 core8/pwb.py mass/eyerounds/geturls

"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

Dir = Path(__file__).parent
urlsfile = Dir / "jsons/urls.json"

import requests
from bs4 import BeautifulSoup


def get_cases_from_url(url):
    """
    Extracts case details from the given URL within the specified div.

    Args:
    url (str): The URL to scrape.

    Returns:
    list: A list of dictionaries, each containing URL, title, and description of a case.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the div with class "row d-flex justify-content-around"
    case_div = soup.find("div", class_="row d-flex justify-content-around")

    # Find all paragraphs containing case descriptions within the specified div
    cases = case_div.find_all("p")
    print(f"Found {len(cases)} cases.")

    # Extract and store case details
    case_details = []
    for case in cases:
        case_dict = {}
        case_link = case.find("a")
        # ---
        if case_link:
            # Extract case details from href tags
            href = case_link["href"]
            # ---
            if not href.startswith("http"):
                href = "https://eyerounds.org/" + href
            # ---
            case_dict["url"] = href
            case_dict["title"] = case_link.get_text().strip()
            case_dict["description"] = case.get_text(strip=True).replace(case_dict["title"], "").strip()

        case_details.append(case_dict)

    return case_details


def start():
    # Define the URL
    url = "https://eyerounds.org/cases.htm"

    # Step 1: Open the URL
    print(f"Step 1: Open URL: {url}")

    response = requests.get(url)
    print(f"Step 1: Opened the URL. Status Code: {response.status_code}")

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    print("Step 2: Parsed the HTML content.")

    # Find all divs with class "col-xs-12 col-sm-6 col-md-6 col-lg-4"
    divs = soup.find_all("div", class_="col-xs-12 col-sm-6 col-md-6 col-lg-4")

    # Initialize a dictionary to store URLs
    with open(urlsfile, "r", encoding="utf-8") as f:
        urls_dict = json.load(f)
    add_new = 0
    # Iterate through each div
    for n, div in enumerate(divs, 1):
        # Extract href and title
        href = div.find("a")["href"]
        if not href.startswith("http"):
            href = "https://eyerounds.org/" + href
        title = div.find("strong").text.strip()

        # Add title to the dictionary with URL
        tab = {"title": title, "url": href, "cases": {}}
        tab["cases"] = get_cases_from_url(href)

        print(f"url {n}/{len(divs)}: {href} has {len(tab['cases'])} cases")
        if href not in urls_dict:
            add_new += 1
            urls_dict[href] = tab

    # Save urls to JSON file
    with open(urlsfile, "w", encoding="utf-8") as f:
        json.dump(urls_dict, f, indent=2)

    print(f"{add_new} new urls added to urls.json")
    print("URLs saved to urls.json")


if __name__ == "__main__":
    start()
