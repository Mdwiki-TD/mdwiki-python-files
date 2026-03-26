"""
# ---
from apis import user_accounts
# ---
username = user_accounts.bot_username     #user_accounts.my_username
password = user_accounts.bot_password     #user_accounts.mdwiki_pass
lgpass_enwiki   = user_accounts.lgpass_enwiki
user_agent   = user_accounts.user_agent
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
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")

my_password = lgpass_enwiki

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
