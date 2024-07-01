"""
from fix_cs1.bots.pmid import pmid_journal

https://pubmed.ncbi.nlm.nih.gov/29083719/

python pwb.py pub type:PMC id:29083719
"""
import re
import requests
import sys
import wikitextparser as wtp
from newapi import printe


def get_pmid_json(pmid):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={pmid}&resulttype=core&format=json"
    # ---
    # get url content
    try:
        content = requests.get(url)
        data = content.json()
        return data
    except Exception as e:
        printe.output(f"Error: {e}")
        return {}


def pmid_journal(pmid, param):
    # ---
    journal = ""
    # ---
    result = get_pmid_json(pmid)
    # ---
    _data_exmple = {
        "pmid": "29083719",
        "bookOrReportDetails": {
            "publisher": "StatPearls Publishing, Treasure Island (FL)",
            "yearOfPublication": 2023,
            "comprisingTitle": "StatPearls",
        },
    }
    # ---
    _data_exmple2 = {
        "doi": "10.1177/0363546508322496",
        "journalInfo": {
            "issue": "11",
            "volume": "36",
            "journalIssueId": 1575497,
            "dateOfPublication": "2008 Nov",
            "monthOfPublication": 11,
            "yearOfPublication": 2008,
            "printPublicationDate": "2008-11-01",
            "journal": {
                "title": "The American journal of sports medicine",
                "medlineAbbreviation": "Am J Sports Med",
                "nlmid": "7609541",
                "isoabbreviation": "Am J Sports Med",
                "essn": "1552-3365",
                "issn": "0363-5465",
            },
        },
    }
    if not result:
        printe.output(f"no result for |{param}={pmid}")
        return journal
    # ---
    hit = result.get("resultList", {}).get("result", [])
    if not hit:
        printe.output(f"no hit for |{param}={pmid}")
        printe.output(result)
        return journal
    # ---
    da_true = {}
    # ---
    for n, da in enumerate(hit):
        id_in = da.get(param, "")
        # ---
        if id_in == pmid:
            da_true = da
            break
    # ---
    journal = da_true.get("bookOrReportDetails", {}).get("comprisingTitle", "")
    # ---
    if not journal:
        journal = da_true.get("journalInfo", {}).get("journal", {}).get("title", "")
    # ---
    if journal:
        printe.output(f"{n}/{len(hit)}: <<green>> id_in: {id_in} - journal: {journal}")
    else:
        printe.output(f"{n}/{len(hit)}: <<red>> |{param}={pmid} - journal: {journal}")
    # ---
    return journal
