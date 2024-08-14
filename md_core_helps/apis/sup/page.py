"""

python3 core8/pwb.py mw_api/page

"""
import logging

logging.basicConfig(level=logging.WARNING)

from newapi import printe
from apis.sup.su_login import Get_MwClient_Site

if __name__ == "__main__":
    from newapi import useraccount
    from apis import user_account_new
    from ncc_core import user_info

    en_site = Get_MwClient_Site("en", "wikipedia", useraccount.username, useraccount.password)

    printe.output("_______________________")

    md_site = Get_MwClient_Site("www", "mdwiki", user_account_new.my_username, user_account_new.mdwiki_pass)

    printe.output("_______________________")

    md_site = Get_MwClient_Site("www", "nccommons", user_info.username, user_info.password)
