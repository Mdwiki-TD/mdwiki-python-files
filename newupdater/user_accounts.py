"""
# ---
import user_accounts
username = user_accounts.my_username
password = user_accounts.mdwiki_pass
user_agent = user_accounts.user_agent

# ---
"""

import os

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")

mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
