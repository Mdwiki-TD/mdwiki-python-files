import os
import sys

from dotenv import load_dotenv
from logger_config import setup_logging as _setup_logging  # type: ignore

try:
    load_dotenv()
except Exception as e:
    print(e)

user_script_paths = [
    "I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/",
    "I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/pybot/src/",
]

if os.getenv("APP_ENV") == "production":
    user_script_paths = [
        "/data/project/mdwiki",
        "/data/project/mdwiki/pybot",
    ]

_ver = sys.version_info[:3]
_python_v = str(_ver[0]) + str(_ver[1]) + str(_ver[2])

_red_ = "\033[91m%s\033[00m"
_blue_ = "\033[94m%s\033[00m"

print(_blue_ % "PYTHON VERSION" + ": " + _red_ % _python_v)

for _u_path in user_script_paths.copy():
    if os.path.exists(_u_path):
        sys.path.append(os.path.abspath(_u_path))
    else:
        print(f"user-config.py, path not exists:{_red_ % _u_path}")

_bots = [
    "__main__",
    "copy_text",
    "copy_to_en",
    "db",
    "find_replace_bot",
    "fix_use",
    "md_core",
    "md_core_helps",
    "mdwiki_api",
    "named_param",
    "newapi",
    "newupdater",
    "td_core",
    "wprefs",
]

for _bot in _bots:
    _setup_logging(name=_bot, level="INFO")
