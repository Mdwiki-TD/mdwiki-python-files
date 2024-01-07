"""
from mdpy.bots.check_title import valid_title #valid_title(title)
"""

falses = ['category:', 'file:', 'template:', 'user:', 'wikipedia:']


def valid_title(title):
    # ---
    title = title.lower().strip()
    # ---
    if title.find('(disambiguation)') != -1:
        return False
    # ---
    # if title.startswith('category:') or title.startswith('file:') or title.startswith('template:') or title.startswith('user:'):
    return not any(title.startswith(prefix) for prefix in falses)
