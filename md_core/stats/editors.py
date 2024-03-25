"""

from stats.editors import get_editors

"""

import json
import os
import re
import sys
from pathlib import Path

from api_sql import wiki_sql
from pymysql.converters import escape_string
# ---
from stats.ar import get_ar_results

Dir = Path(__file__).parent
editors_dir = Dir / "editors"

# make dir editors
if not os.path.exists(Dir / "editors"):
    os.mkdir(Dir / "editors")


def validate_ip(ip_address):
    if ip_address == "CommonsDelinker":
        return True
    # IPv4 pattern
    ipv4_pattern = r"^\b(?:\d{1,3}\.){3}\d{1,3}\b$"
    # IPv6 pattern
    ipv6_pattern = r"^\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b$"

    if re.match(ipv4_pattern, ip_address):
        return True
    elif re.match(ipv6_pattern, ip_address):
        return True
    return False


def get_editors_sql(links, site):
    # ---
    qua = """
        SELECT actor_name, count(*) as count from revision
            join actor on rev_actor = actor_id
            join page on rev_page = page_id
            WHERE lower(cast(actor_name as CHAR)) NOT LIKE '%bot%' AND page_namespace = 0 AND rev_timestamp like '2023%'
            and page_id in (
            select page_id
            from page
                where page_title in (
                    %s
                )
            )
        group by actor_id
        order by count(*) desc
    """
    # ---
    editors = {}
    # ---
    for i in range(0, len(links), 100):
        # ---
        pages = links[i:i + 100]
        # ---
        # lim = ' , '.join(['?' for x in pages])
        lim = ",".join([f'"{escape_string(x)}"' for x in pages])
        # ---
        qua2 = qua.replace("%s", lim)
        # ---
        # print(qua2)
        # ---
        edits = wiki_sql.sql_new(qua2, site)
        # ---
        for x in edits:
            # ---
            actor_name = x["actor_name"]
            # ---
            # skip if actor_name iis IP address
            if validate_ip(actor_name):
                continue
            # ---
            if actor_name not in editors:
                editors[actor_name] = 0
            # ---
            editors[actor_name] += x["count"]
            # ---
        # ---
    return editors


def get_editors(links, site):
    editors = {}
    # ---
    if os.path.exists(editors_dir / f"{site}.json"):
        with open(editors_dir / f"{site}.json", encoding="utf-8") as f:
            editors = json.load(f)
            return editors
    # ---
    if site == "ar":
        editors = get_ar_results()
    else:
        editors = get_editors_sql(links, site)
    # ---
    if "dump" in sys.argv and editors:
        with open(editors_dir / f"{site}.json", "w", encoding="utf-8") as f:
            json.dump(editors, f, sort_keys=True)
    # ---
    return editors
