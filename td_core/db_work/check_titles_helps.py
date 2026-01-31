#!/usr/bin/python3
"""
from db_work.check_titles_helps import get_new_target_log, Find_pages_exists, WikiPage, users_infos
"""
import logging

from newapi.wiki_page import NEW_API, MainPage

logger = logging.getLogger(__name__)


def get_new_target_log(lang, target):
    # ---
    deleted = False
    # ---
    done = []
    # ---
    to_check = target
    # ---
    api_new1 = NEW_API(lang, family="wikipedia")
    # ---
    logger.info(f"get_new_target_log() lang:{lang}, target:{target}")
    # ---
    n = 0
    # ---
    while to_check != "":
        # ---
        n += 1
        # ---
        logger.info(f"<<blue>> get_new_target_log({n}) lang:{lang}, target:{target}")
        # ---
        logs = api_new1.get_logs(to_check)
        # ---
        new = ""
        # ---
        for log in logs:
            action = log.get("action", "")
            title = log.get("title", "")
            # ---
            if action == "delete" and title == target:
                deleted = True
            # ---
            new = log.get("params", {}).get("target_title", "")
            # ---
            if new:
                break
        # ---
        if new:
            done.append(to_check)
            logger.info(f"> title:{to_check} moved to:{new}")
            to_check = new
        else:
            break
        # ---
        if to_check in done:
            logger.info(f"to_check:{to_check} in done")
            break
    # ---
    logger.info(f"get_new_target_log() lang:{lang}, target:{target}, new:{to_check}")
    # ---
    return deleted, to_check


def Find_pages_exists(lang, titles):
    api_newx = NEW_API(lang, family="wikipedia")
    pages = api_newx.Find_pages_exists_or_not(titles, get_redirect=True)
    # ---
    return pages


def users_infos(lang, users):
    api_newx = NEW_API(lang, family="wikipedia")
    result = api_newx.users_infos(ususers=users)
    # ---
    return result


def WikiPage(title, lang, family="wikipedia"):
    return MainPage(title, lang, family=family)
