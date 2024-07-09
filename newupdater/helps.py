"""
from wprefs.helps import print_s, ec_de_code, exepts
"""
import sys
import traceback
import urllib.parse

try:
    import pywikibot
except ImportError:
    pywikibot = None


def print_s(s):
    if 'from_toolforge' not in sys.argv:
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
    if not pywikibot:
        return
    if 'from_toolforge' not in sys.argv:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
