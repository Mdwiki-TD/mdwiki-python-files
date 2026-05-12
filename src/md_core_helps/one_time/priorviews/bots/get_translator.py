"""

python3 core8/pwb.py priorviews/bots/get_translator

"""

import logging
import sys
from urllib.parse import urlencode

import requests
from priorviews.bots import helps

logger = logging.getLogger(__name__)

# ---
"""
# ---
from priorviews.bots import get_translator
# tt = get_translator.get_au(title, lang)
# ---
"""
# ---
# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# ---


class FindTranslator:
    def __init__(self, title, lang="en"):
        # ---
        self.lang = lang
        self.title = title
        self.url = f"https://{self.lang}.wikipedia.org/w/api.php"
        self.translator = ""
        # ---
        self.session = requests.Session()
        # ---
        self.start()

    def post_to_json(self, params):
        json1 = {}
        # ---
        unurl = f"{self.url}?{urlencode(params)}"
        # ---
        if "printurl" in sys.argv and "text" not in params:
            logger.info(f"get_old:\t\t{unurl}")
        # ---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            logger.error(f"except: lang:{self.lang} {e}")
        # ---
        return json1

    def start(self):
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title,
            "formatversion": "2",
            "rvprop": "comment|user",
            "rvdir": "newer",
            "rvlimit": "max",
        }
        # ---
        rvcontinue = "x"
        # ---
        while rvcontinue != "":
            # ---
            if rvcontinue != "x":
                params["rvcontinue"] = rvcontinue
            # ---
            json1 = self.post_to_json(params)
            # ---
            rvcontinue = json1.get("continue", {}).get("rvcontinue", "")
            # ---
            pages = json1.get("query", {}).get("pages", [{}])
            # ---
            for p in pages:
                revisions = p.get("revisions", [])
                for r in revisions:
                    # logger.info(r)
                    user = r.get("user", "")
                    if user == "" or helps.is_ip(user):
                        continue
                    # ---
                    comment = r.get("comment", "").lower()
                    if helps.isv(comment):
                        # logger.info(r)
                        self.translator = user
                        return

    def Translator(self):
        logger.info(f"\t\t : {self.translator}")
        return self.translator


def get_au(title, lang):
    # ---
    bot = FindTranslator(title, lang=lang)
    # ---
    auu = bot.Translator()
    # ---
    return auu


# ---
if __name__ == "__main__":
    # ---
    t = get_au("نكاف", "ar")
    logger.info(f"au: {t}")
    sys.exit()
    # ---
