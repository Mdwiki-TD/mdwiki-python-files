""" """

import os
from dotenv import load_dotenv
load_dotenv()

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")

mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")
my_password = lgpass_enwiki

username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")
qs_token = os.getenv("QS_TOKEN")

bot_username = username
bot_password = password

if qs_token and not qs_token.startswith("$2y$10$"):
    qs_token = "$2y$10$" + qs_token

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
