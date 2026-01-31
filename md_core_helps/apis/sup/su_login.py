"""
from apis.sup.su_login import Get_MwClient_Site
"""

import logging
import os
import sys
from http.cookiejar import MozillaCookieJar

import mwclient
import requests
from apis.sup.cookies_bot import get_file_name
from mwclient.client import Site

logger = logging.getLogger(__name__)


def default_user_agent():
    tool = os.getenv("HOME")
    if tool:
        # "/data/project/mdwiki"
        tool = tool.split("/")[-1]
    else:
        tool = "himo"
    # ---
    li = f"{tool} bot/1.0 (https://{tool}.toolforge.org/; tools.{tool}@toolforge.org)"
    # ---
    # logger.info(f"default_user_agent: {li}")
    # ---
    return li


user_agent = default_user_agent()


def Get_MwClient_Site(lang, family, username, password):
    cookies_file = get_file_name(lang, family, username)

    domain = f"{lang}.{family}.org"

    cookie_jar = MozillaCookieJar(cookies_file)

    connection = requests.Session()
    connection.headers["User-Agent"] = user_agent

    if os.path.exists(cookies_file):
        logger.info("<<yellow>>loading cookies")
        try:
            # Load cookies from file, including session cookies
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            connection.cookies = cookie_jar  # Tell Requests session to use the cookiejar.
        except Exception as e:
            logger.error("Could not load cookies: %s" % e)

    if "dopost" in sys.argv:
        site = Site(domain, clients_useragent=user_agent, pool=connection)
    else:
        try:
            site = Site(domain, clients_useragent=user_agent, pool=connection)
        except Exception as e:
            logger.error(f"Could not connect to ({domain}): %s" % e)
            return False

    if not site.logged_in:
        logger.info(f"<<yellow>>logging in to ({domain}), username: {username}")
        try:
            site.login(username=username, password=password)
        except mwclient.errors.LoginError as e:
            logger.error(f"Could not login to ({domain}): %s" % e)

    if site.logged_in:
        logger.info(f"<<yellow>>logged in as {site.username} to ({domain})")

    # Save cookies to file, including session cookies
    cookie_jar.save(ignore_discard=True, ignore_expires=True)

    return site
