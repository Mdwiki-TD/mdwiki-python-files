"""

"""

import sys
import os

from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

bot_username = os.getenv("WIKIPEDIA_BOT_USERNAME")
bot_password = os.getenv("WIKIPEDIA_BOT_PASSWORD")

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME")
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD")
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD")

username = bot_username
password = bot_password

if "workhimo" in sys.argv:
    username = my_username
    password = lgpass_enwiki
