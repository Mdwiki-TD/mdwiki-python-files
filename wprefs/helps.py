"""
from wprefs.helps import print_s, ec_de_code, exepts
"""

import logging
import sys
import traceback
import urllib.parse

logger = logging.getLogger(__name__)


def print_s(s):
    if "returnfile" not in sys.argv:
        logger.info(s)


def ec_de_code(tt, type1):
    fao = tt
    if type1 == "encode":
        # fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif type1 == "decode":
        fao = urllib.parse.unquote(tt)
    return fao


def exepts():
    if "returnfile" not in sys.argv:
        logger.error("Traceback (most recent call last):")
        logger.error(traceback.format_exc())
        logger.error("CRITICAL:")
