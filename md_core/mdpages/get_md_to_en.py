"""

# python3 core8/pwb.py mdpages/get_md_to_en nodump
# python3 core8/pwb.py mdpages/get_md_to_en -others nodump

"""
import sys
from pathlib import Path
# ---
from mdpages import qids_help
# qids_help.get_o_qids_new(o_qids, t_qids_in)
# qids_help.get_pages_to_work(ty="td|other")
# qids_help.check(work_list, all_pages)


def start():
    ty = "other" if "-others" in sys.argv else "td"
    # ---
    to_work, all_pages = qids_help.get_pages_to_work(ty)
    # ---
    qids_help.check(to_work, all_pages, ty)


if __name__ == "__main__":
    start()
