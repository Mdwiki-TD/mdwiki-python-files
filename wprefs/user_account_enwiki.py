"""
# ---
from wprefs import user_account_enwiki
user_agent    = user_account_enwiki.user_agent
# ---
"""

import configparser
import os

home_dir = os.getenv("HOME")
dir2 = home_dir if home_dir else "I:/mdwiki/mdwiki"
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

botusername = config["DEFAULT"].get("botusername", "")
botpassword = config["DEFAULT"].get("botpassword", "")

my_username = config["DEFAULT"].get("my_username", "")
user_agent = config["DEFAULT"].get("user_agent", "")
