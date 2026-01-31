"""

from fix_use.write_bot import write# write(oldtext, text, filepath)

"""

import sys

from newapi import printe

ASK_all = True


# ---
def write(oldtext, text, filepath):
    global ASK_all
    # ---
    if oldtext == text:
        path2 = filepath.split("/")[-1]
        printe.output(f"No change in {path2}")
        return False
    # ---
    printe.showDiff(oldtext, text)
    # ---
    printe.output(filepath.replace("/", "\\"))
    # ---
    do_save = False
    # ---
    if ASK_all:
        # ---
        printe.output("<<green>> Save?")
        ask = input(f"save new text?...{filepath}:")
        if ask in ["", "a", "y"]:
            print("save new text")
            # ---
            do_save = True
        # ---
        elif ask == "x":
            sys.exit()
        else:
            print(f"answer is wrong:{ask}, return False")
            return False
        # ---
        if ask == "a":
            ASK_all = False
    else:
        do_save = True
    # ---
    if do_save:
        # ---
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        printe.output("<<green>> save done..")
        # ---
        return text

    return False
