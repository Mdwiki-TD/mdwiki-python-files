"""

"""

import os
from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

username = os.getenv("WIKIPEDIA_BOT_USERNAME")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

bot_username = username
bot_password = password

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")
