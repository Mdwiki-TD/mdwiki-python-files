""" """

import os
from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")

mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")

bot_username = os.getenv("WIKIPEDIA_BOT_USERNAME")
bot_password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

user_agent = "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"

User_tables = {
    "username": my_username,
    "password": mdwiki_pass,
}

User_tables_wiki = {
    "username": bot_username,
    "password": bot_password,
}
