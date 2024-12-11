#!/usr/bin/python3
"""

python3 core8/pwb.py copy_to_en/to_file

"""
import json
import requests
from newapi import printe
from pathlib import Path
from copy_to_en.medwiki import get_text

dir1 = Path(__file__).parent
Dir = "/data/project/mdwiki/public_html/mdtexts"

if str(dir1).find("I:") != -1:
    Dir = "I:/mdwiki/mdwiki/public_html/mdtexts"


def html_to_segements(text):
    url = "https://ncc2c.toolforge.org/textp"
    headers = {"Content-Type": "application/json"}
    payload = {"html": text}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        result = response_data.get("result", None)
        return result
    except requests.exceptions.RequestException as e:
        printe.error(f"html_to_segements(): Error occurred: {e}")
        return None


def convert_wikitext_to_html(text):
    end_point = "https://en.wikipedia.org/api/rest_v1/transform/wikitext/to/html/Sandbox"

    params = {"wikitext": text}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(end_point, headers=headers, data=json.dumps(params))
        # response.raise_for_status()  # Raise an error for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        printe.error(f"convert_wikitext_to_html(): Error occurred: {e}")
        return None


def save_text(text, file):
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        printe.error(f"save_text(): Exception: {e}")


def get_page_text(x, x2):
    newtext, revid = get_text(x)
    # ---
    file = Dir + "/wikitext/" + x2 + ".txt"
    # ---
    save_text(newtext, file)
    # ---
    return newtext


def to_html(newtext, x, x2):
    # ---
    html = convert_wikitext_to_html(newtext)
    # ---
    file = Dir + "/html/" + x2 + ".html"
    # ---
    save_text(html, file)
    # ---
    return html


def to_segements(html_text, x2):
    # ---
    segements = html_to_segements(html_text)
    # ---
    file = Dir + "/segments/" + x2 + ".html"
    # ---
    save_text(segements, file)
    # ---
    return segements


def one_page_new(x):
    x2 = x.replace(" ", "_").replace("'", "_").replace(":", "_").replace("/", "_").replace('"', "_")
    # ---
    text = get_page_text(x, x2)
    # ---
    html_text = to_html(text, x, x2)
    # ---
    seg_text = to_segements(html_text, x2)


if __name__ == "__main__":
    one_page_new("Menopause")
