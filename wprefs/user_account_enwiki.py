"""
# ---
from wprefs import user_account_enwiki
lgpass_enwiki = user_account_enwiki.lgpass_enwiki
user_agent    = user_account_enwiki.user_agent
# ---
"""

import configparser

from pathlib import Path

Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

my_username = config["DEFAULT"].get("my_username", "")
lgpass_enwiki = config["DEFAULT"].get("lgpass_enwiki", "")
user_agent = config["DEFAULT"].get("user_agent", "")
