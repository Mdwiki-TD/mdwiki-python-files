""" """

import os
import sys

from dotenv import load_dotenv

try:
    load_dotenv()
except Exception:
    pass

bot_username = os.getenv("WIKIPEDIA_BOT_USERNAME") or ""
bot_password = os.getenv("WIKIPEDIA_BOT_PASSWORD") or ""

my_username = os.getenv("WIKIPEDIA_HIMO_USERNAME") or ""
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD") or ""
lgpass_enwiki = os.getenv("WIKIPEDIA_HIMO_PASSWORD") or ""

username = bot_username
password = bot_password

if "workhimo" in sys.argv:
    username = my_username
    password = lgpass_enwiki
