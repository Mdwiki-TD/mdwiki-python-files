"""

python3 core8/pwb.py apis/sup/page

"""

import logging

from apis.sup.su_login import Get_MwClient_Site

logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    from apis import user_accounts

    username = user_accounts.bot_username  # user_accounts.my_username
    password = user_accounts.bot_password  # user_accounts.mdwiki_pass

    md_site = Get_MwClient_Site("www", "wikidata", username, password)
