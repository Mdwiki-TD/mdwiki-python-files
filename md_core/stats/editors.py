'''

from stats.editors import get_editors

'''
import json
import re
import os
import sys
from pymysql.converters import escape_string
# ---
from api_sql import wiki_sql


def get_editors(links, site):
    # ---
    qua = '''
        SELECT actor_name, count(*) from revision 
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
    '''
    # ---
    editors = {}
    # ---
    for i in range(0, len(links), 100):
        # ---
        pages = links[i:i+100]
        # ---
        qua = qua % (' , '.join(['?' for x in pages]))
        # ---
        edits = wiki_sql.sql_new(qua, site, values=pages)
        # ---
        for x in edits:
            # ---
            actor_name = x['actor_name']
            # ---
            if actor_name not in editors:
                editors[actor_name] = 0
            # ---
            editors[actor_name] += x['count']
            # ---
        # ---
    return editors

def get_editors_x(links, site):
    # ---
    qua = '''
        SELECT actor_name, count(*) from revision 
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
    '''
    # ---
    editors = {}
    # ---
    for i in range(0, len(links), 100):
        # ---
        pages = links[i : i + 100]
        # ---
        qua = qua % (','.join([f'"{escape_string(x)}"' for x in pages]))
        # ---
        edits = wiki_sql.sql_new(qua, site)
        # ---
        for x in edits:
            # ---
            actor_name = x['actor_name']
            # ---
            if actor_name not in editors:
                editors[actor_name] = 0
            # ---
            editors[actor_name] += x['count']
            # ---
        # ---
    return editors
