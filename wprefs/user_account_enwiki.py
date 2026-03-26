"""
# ---
from wprefs import user_account_enwiki
lgpass_enwiki = user_account_enwiki.lgpass_enwiki
user_agent    = user_account_enwiki.user_agent
# ---
"""

import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

bot_username = username
bot_password = password

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
