#!/usr/bin/python3
"""
# ---
from mdpy.bots import rest_v1_views
# rest_v1_views.get_views_last_30_days(langcode, titles)
# ---
"""

#
# (C) Ibrahem Qasim, 2022
#
#
import json
import traceback
import pywikibot
import sys
import urllib.parse
import datetime
from datetime import timedelta

# ---
from pywikibot.comms import http
from mdpy import printe


def get_views_last_30_days(langcode, titles):
    # ---
    numbers = {}
    # ---
    endDate = datetime.datetime.utcnow() - timedelta(days=1)
    startDate = endDate - timedelta(weeks=4)
    # ---
    endDate = endDate.strftime('%Y%m%d%H')
    startDate = startDate.strftime('%Y%m%d%H')
    # ---
    numb = 0
    # ---
    for page in titles:
        # ---
        numb += 1
        # ---
        # print when numb % 100 == 0
        if numb % 100 == 0:
            print(f'get_views_with_rest_v1: {numb}/{len(titles)}')
        # ---
        if 'limit5' in sys.argv and numb > 5:
            break
        # ---
        pa = urllib.parse.quote(page)
        # ---
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{langcode}.wikipedia/all-access/all-agents/{pa.replace('/', '%2F')}/daily/{startDate}/{endDate}"
        # ---
        if "printurl" in sys.argv:
            printe.output(f"printboturl:\t\t{url}")
        # ---
        req = http.fetch(url)
        # req = requests.Session().get( url )
        # ---
        st = req.status_code
        # ---
        if 500 <= st < 600 or st == 404:
            printe.output(f'received {st} status from:')
            printe.output(url)
        # ---
        data = {}
        try:
            data = json.loads(req.text)
        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(req.text)
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
        # ---
        if not data:
            pywikibot.output(url)
        # ---
        _sadasd = [{"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021070100", "access": "all-access", "agent": "all-agents", "views": 77}, {"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021080100", "access": "all-access", "agent": "all-agents", "views": 95}]
        # ---
        numbers[page] = sum(x["views"] for x in data.get('items', []))
    # ---
    return numbers
