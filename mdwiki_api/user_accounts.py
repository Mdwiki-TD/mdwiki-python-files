""" """

import os
from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")

mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")
my_password = lgpass_enwiki

username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

bot_username = username
bot_password = password

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
# ---
User_tables = {
    "username": my_username,
    "password": mdwiki_pass,
}

User_tables_wiki = {
    "username": bot_username,
    "password": bot_password,
}

SITECODE = "www"
FAMILY = "mdwiki"
