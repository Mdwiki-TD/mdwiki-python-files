import os
import pywikibot
from MedWorkNew import work_on_text
from pathlib import Path

def test():
    # ---
    # python3 pwb.py newupdater/MedWorkNew
    
    Dir = Path(__file__).parent
    # ---
    with open(os.path.join(Dir, "bots/resources.txt"), "r", encoding="utf-8") as f:
        text = f.read()
    # ---
    newtext = work_on_text("test", text)
    # ---
    pywikibot.showDiff(text, newtext)
    # ---
    with open(os.path.join(Dir, "bots/resources_new.txt"), "w", encoding="utf-8") as f:
        f.write(newtext)
    # ---


if __name__ == "__main__":
    test()
