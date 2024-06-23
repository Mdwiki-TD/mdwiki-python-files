"""
python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi get:5 ask nodudb norevip

tfj run fiaa6 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi nodudb get:6"
tfj run fiaa4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all del2 norevip noapi nodudb get:4"


python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi studies_titles2

tfj run sst2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all noapi studies_titles2"

python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi reverse
python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi norevip reverse
python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi norevip

tfj run fix9 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/new_all del2 noapi nodb get:9"

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
from fix_mass.jsons.files import studies_titles, studies_titles2
from fix_mass.fix_sets.lists.studies_fixed import studies_fixed_done


def ddo(taba):
    ids = taba
    tabs = {}
    # ---
    Done = []
    # ---
    if "nodone" not in sys.argv:
        Done = studies_fixed_done
    # ---
    after_done = [x for x in ids if x not in Done]
    # ---
    print(f"all ids: {len(ids)}, after done: {len(after_done)}")
    # ---
    ids = after_done
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
    # ---
    if "studies_titles2" in sys.argv:
        ids = list(studies_titles2.keys())
    # ---
    ids = ddo(ids)
    # ---
    ids.sort()
    # ---
    if "reverse" in sys.argv:
        ids.reverse()
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    # ---
    for study_id in ids:
        work_one_study(study_id)


if __name__ == "__main__":
    main()
