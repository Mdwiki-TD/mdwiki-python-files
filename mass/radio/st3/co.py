'''

python3 /data/project/mdwiki/pybot/mass/radio/st3/co.py

'''
import sys
import os
user_script_paths = [
    '/data/project/mdwiki',
    '/data/project/mdwiki/pybot',
    '/data/project/mdwiki/pybot/md_core',
]
for _u_path in user_script_paths:
    if os.path.exists(_u_path):
        sys.path.append(os.path.abspath(_u_path))

from mass.radio.st3.count import start

start()
