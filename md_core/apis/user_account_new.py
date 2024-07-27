"""
# ---
from apis import user_account_new
# ---
username = user_account_new.bot_username     #user_account_new.my_username
password = user_account_new.bot_password     #user_account_new.my_password      #user_account_new.mdwiki_pass
lgname_enwiki   = user_account_new.lgname_enwiki
lgpass_enwiki   = user_account_new.lgpass_enwiki
user_agent   = user_account_new.user_agent
# ---
"""

# import sys
# import os
import configparser

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

username = config["DEFAULT"].get("botusername", "")
password = config["DEFAULT"].get("botpassword", "")

bot_username = config["DEFAULT"].get("botusername", "")
bot_password = config["DEFAULT"].get("botpassword", "")

my_username = config["DEFAULT"].get("my_username", "")
my_password = config["DEFAULT"].get("my_password", "")

mdwiki_pass = config["DEFAULT"].get("mdwiki_pass", "")

lgname_enwiki = config["DEFAULT"].get("lgname_enwiki", "")
lgpass_enwiki = config["DEFAULT"].get("lgpass_enwiki", "")

qs_token = config["DEFAULT"].get("qs_token", "")

user_agent = config["DEFAULT"].get("user_agent", "")
