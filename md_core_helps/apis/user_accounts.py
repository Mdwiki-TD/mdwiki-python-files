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

import configparser
import os

home_dir = os.getenv("HOME")
dir2 = home_dir if home_dir else "I:/mdwiki/mdwiki"
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

username = config["DEFAULT"].get("botusername", "")
password = config["DEFAULT"].get("botpassword", "")

bot_username = config["DEFAULT"].get("botusername", "")
bot_password = config["DEFAULT"].get("botpassword", "")

my_username = config["DEFAULT"].get("my_username", "")

mdwiki_pass = config["DEFAULT"].get("mdwiki_pass", "")

lgpass_enwiki = config["DEFAULT"].get("lgpass_enwiki", "")
my_password = lgpass_enwiki

qs_token = config["DEFAULT"].get("qs_token", "")

user_agent = config["DEFAULT"].get(
    "user_agent", "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
)
