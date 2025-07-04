"""
# ---
from mdpy.bots import py_tools
# py_tools.ec_de_code( tt , type )
# py_tools.Decode_bytes(x)
# py_tools.quoteurl(fao)
# ---
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys
import urllib
from newapi.except_err import exception_err

# ---
PYTHON_VERSION = sys.version_info[:3]
if PYTHON_VERSION >= (3, 9):
    removeprefix = str.removeprefix  # type: ignore[attr-defined]
    removesuffix = str.removesuffix  # type: ignore[attr-defined]
else:

    def removeprefix(string: str, prefix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        return string[len(prefix):] if string.startswith(prefix) else string

    def removesuffix(string: str, suffix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        return string[: -len(suffix)] if string.endswith(suffix) else string


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
        exception_err(e)
    # ---
    if endash:
        fao = fao.replace("ioioioioio", "%E2%80%93")
    # ---
    return fao


def Decode_bytes(x):
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    return x


def ec_de_code(tt, Type):
    fao = tt
    if Type == 'encode':
        # fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif Type == 'decode':
        fao = urllib.parse.unquote(tt)
    return fao


# ---
