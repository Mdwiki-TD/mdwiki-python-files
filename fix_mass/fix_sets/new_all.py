"""
python3 core8/pwb.py fix_mass/fix_sets/new_all

tfj run fixg1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:1 9725"
tfj run fixg2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:2 9725"
tfj run fixg3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:3 9725"
tfj run fixg4 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:4 9725"
tfj run fixg5 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:5 9725"
tfj run fixg6 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:6 9723"

"""
import sys

from newapi import printe
from fix_mass.fix_sets.new import work_one_study
from fix_mass.jsons.files import studies_titles


def ddo(taba):
    ids = taba
    tabs = {}
    # ---
    print(f"all ids: {len(ids)}")
    # ---
    length = (len(ids) // 10) + 1
    # ---
    for i in range(0, len(ids), length):
        num = i // length + 1
        # ---
        tabs[str(num)] = ids[i : i + length]
        # ---
        command = f'tfj run fix{num} --image python3.9 --command "'
        command += f"$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all get:{num} {len(tabs[str(num)])}"
        command += '"'
        # ---
        print(command)
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "get":
            ids = tabs[value]
            print(f"work in {len(ids)} ids")
    del tabs

    return ids


def main():
    # ---
    ids = list(studies_titles.keys())
    ids = ddo(ids)
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    # ---
    for study_id in ids:
        work_one_study(study_id)


if __name__ == "__main__":
    main()
