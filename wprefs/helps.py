"""
from wprefs.helps import print_s, ec_de_code, exepts
"""
import sys
import traceback
import urllib.parse

try:
    from newapi import printe
except ImportError:
    printe = None


def print_s(s):
    if 'returnfile' not in sys.argv:
        print(s)


def ec_de_code(tt, type1):
    fao = tt
    if type1 == 'encode':
        # fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif type1 == 'decode':
        fao = urllib.parse.unquote(tt)
    return fao


def exepts():
    if not printe or not hasattr(printe, "error"):
        return
    if 'returnfile' not in sys.argv:
        printe.error('Traceback (most recent call last):')
        printe.error(traceback.format_exc())
        printe.error('CRITICAL:')
