""" """

import logging
import urllib
import urllib.parse

logger = logging.getLogger(__name__)


def quoteurl(fao):
    endash = False
    # ---
    # url2 = urllib.parse.quote_plus(url)
    # ---
    if fao.find("–") != -1:
        endash = True
        fao = fao.replace("–", "ioioioioio")
    # ---
    try:
        fao = urllib.parse.quote(fao)
    except Exception as e:
        logger.exception("Exception:", exc_info=True)
    # ---
    if endash:
        fao = fao.replace("ioioioioio", "%E2%80%93")
    # ---
    return fao


def Decode_bytes(x):
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    return x


def ec_de_code(tt, _type):
    fao = tt
    if _type == "encode":
        # fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif _type == "decode":
        fao = urllib.parse.unquote(tt)
    return fao
