#!/usr/bin/python3
"""
# ---
from apis import views_rest
# views_rest.get_views_with_rest_v1(langcode, titles, date_start="20150701", date_end="20300101", printurl=False, printstr=False, Type="daily")
# views_rest.get_views_last_30_days(langcode, titles)
# ---
"""
import json
import tqdm
import sys
import urllib
import urllib.parse
from pywikibot.comms import http
import datetime
from datetime import timedelta

from newapi import printe
from newapi.except_err import exception_err


def get_all_data(langcode, titles, date_start, date_end, printurl=False, printstr=False, use_tqdm=True):
    # ---
    status_error = 0
    # ---
    all_data = {}
    # ---
    ux = enumerate(titles, start=1)
    # ---
    if use_tqdm:
        ux = tqdm.tqdm(ux)
    # ---
    for numb, page in ux:
        # ---
        # print when numb % 100 == 0
        # if numb % 100 == 0: print(f"get_views_with_rest_v1: {numb}/{len(titles)}")
        # ---
        if "limit5" in sys.argv and numb > 5:
            break
        # ---
        pa = urllib.parse.quote(page)
        # ---
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{langcode}.wikipedia/all-access/all-agents/{pa.replace('/', '%2F')}/daily/{date_start}/{date_end}"
        # ---
        if "printurl" in sys.argv or printurl:
            printe.output(f"printboturl:\t\t{url}")
        # ---
        if printstr:
            printe.output("-------------------")
            printe.output(f"a {numb}/{len(titles)} page:{page}")
        # ---
        req = http.fetch(url)
        # req = requests.Session().get( url )
        # ---
        st = req.status_code
        # ---
        data = {}
        # ---
        try:
            data = json.loads(req.text)
        except Exception as e:
            if printstr:
                exception_err(e, text=req.text)
        # ---
        if 500 <= st < 600 or st == 404 or not data:
            status_error += 1
            # printe.output(f"received {st} status from:")
            # printe.output(url)
        # ---
        _sadasd = [{"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021070100", "access": "all-access", "agent": "all-agents", "views": 77}, {"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021080100", "access": "all-access", "agent": "all-agents", "views": 95}]
        # ---
        all_data[page] = data.get("items", [])
    # ---
    if status_error > 0:
        printe.output(f"get_views_with_rest_v1: status_error in {status_error}/{len(titles)} pages.")
    # ---
    return all_data


def get_views_with_rest_v1(langcode, titles, date_start="20150701", date_end="20300101", printurl=False, printstr=False, Type="daily", use_tqdm=True):
    # ---
    date_start = f"{date_start}00"
    date_end = f"{date_end}00"
    # ---
    all_data = get_all_data(langcode, titles, date_start, date_end, printurl=printurl, printstr=printstr, use_tqdm=use_tqdm)
    # ---
    numbers = {}
    # ---
    for page, views_items in all_data.items():
        number_all = 0
        # ---
        tabl = {}
        # ---
        for x in views_items:
            # ---
            number_all += x["views"]
            # ---
            month = str(x["timestamp"])[:6]
            year = str(month)[:4]
            # ---
            if year not in tabl:
                tabl[year] = {"all": 0}
            # ---
            tabl[year]["all"] += x["views"]
            # ---
            if month not in tabl[year]:
                tabl[year][month] = 0
            # ---
            tabl[year][month] += x["views"]
            # ---
        # ---
        if number_all > 0:
            numbers[page] = {"all": number_all}
            # ---
            txt = f"all_views:{number_all}"
            # ---
            for year, y_tab in tabl.items():
                if y_tab.get("all", 0) > 0:
                    numbers[page][year] = y_tab
                    txt += f', {year}: {y_tab["all"]}'
            # ---
            if printstr:
                printe.output(txt)
            # ---
    # ---
    return numbers


def get_views_last_30_days(langcode, titles, printurl=False, printstr=False, use_tqdm=True):
    # ---
    date_end = datetime.datetime.utcnow() - timedelta(days=1)
    date_start = date_end - timedelta(weeks=4)
    # ---
    date_end = date_end.strftime("%Y%m%d%H")
    date_start = date_start.strftime("%Y%m%d%H")
    # ---
    all_data = get_all_data(langcode, titles, date_start, date_end, printurl=printurl, printstr=printstr, use_tqdm=use_tqdm)
    # ---
    numbers = {}
    # ---
    for page, views_items in all_data.items():
        numbers[page] = sum(x["views"] for x in views_items)
    # ---
    return numbers


if __name__ == "__main__":
    ux = get_views_with_rest_v1("ar", ["yemen", "صنعاء"], date_start="20040101", date_end="20300101")
    printe.output(ux)
