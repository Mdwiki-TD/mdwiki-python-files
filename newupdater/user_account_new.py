"""
# ---
import user_account_new
username = user_account_new.my_username
password = user_account_new.mdwiki_pass
user_agent = user_account_new.user_agent

# ---
"""

import configparser
import os

home_dir = os.getenv("HOME") or "I:/mdwiki/mdwiki"

config = configparser.ConfigParser()
config.read(f"{home_dir}/confs/user.ini")

my_username = config["DEFAULT"].get("my_username", "")

mdwiki_pass = config["DEFAULT"].get("mdwiki_pass", "")

user_agent = config["DEFAULT"].get(
    "user_agent", "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
)
