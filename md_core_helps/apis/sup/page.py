"""

python3 core8/pwb.py apis/sup/page

"""

import logging

logging.basicConfig(level=logging.WARNING)

from apis.sup.su_login import Get_MwClient_Site

if __name__ == "__main__":
    from apis import user_account_new

    username = user_account_new.bot_username  # user_account_new.my_username
    password = user_account_new.bot_password  # user_account_new.mdwiki_pass

    md_site = Get_MwClient_Site("www", "wikidata", username, password)
