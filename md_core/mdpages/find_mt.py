#!/usr/bin/env python

"""

Usage:

python3 core8/pwb.py mdpages/find_mt

"""

#

import os

import sys

# ---

from mdpy.bots import sql_for_mdwiki

from mdpy.bots import wiki_api

from mdpy.bots import wikidataapi

from mdpy import printe

from mdpy.bots.check_title import valid_title

from mdpy.bots import sql_qids_others

# ---

qids_othrs = sql_qids_others.get_others_qids()

qids = sql_for_mdwiki.get_all_qids()

# ---

to_work = [title for title, q in qids.items() if q == '' and valid_title(title)]

printe.output(f'<<green>> to_work list: {len(to_work)}')

# ---

new_qids = {x: qids_othrs[x] for x in to_work if x in qids_othrs}

printe.output(f'<<green>> new_qids list: {len(new_qids)}')

# ---


def doo():

    # ---

    if len(to_work) == 0:

        printe.output('<<green>> to_work list is empty. return "".')

        return

    # ---

    if len(new_qids) == 0:

        printe.output('<<green>> new_qids list is empty. return "".')

        return

    # ---

    sql_for_mdwiki.add_titles_to_qids(new_qids)


if __name__ == '__main__':

    doo()
