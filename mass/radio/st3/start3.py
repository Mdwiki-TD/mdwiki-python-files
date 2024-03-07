"""

python3 core8/pwb.py mass/radio/st3/start3 test nomulti
python3 /data/project/mdwiki/pybot/mass/radio/st3/start3.py test

"""
import sys
import psutil
import tqdm
import json
if "nomulti" in sys.argv or len(tab) < 10:
    for x in group:
        do_it(x)
else:
    pool = Pool(processes=5)
    pool.map(do_it, group)
    pool.close()
    pool.terminate()
        # ---
        print_memory()
        # ---
        if "nomulti" in sys.argv or len(tab) < 10:
            for x in group:
                do_it(x)
        else:
            pool = Pool(processes=5)
            pool.map(do_it, group)
            pool.close()
            pool.terminate()


def ddo(taba):
    ids_tabs = taba
    tabs = {}
    print(f"all cases: {len(ids_tabs)}")
    length = (len(ids_tabs) // 6) + 1
    for i in range(0, len(ids_tabs), length):
        num = i // length + 1
        tabs[str(num)] = dict(list(ids_tabs.items())[i : i + length])
        # print(f'tab {num} : {len(tabs[str(num)])}')
        print(f'tfj run mu{num} --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/start3 nodiff get:{num} {len(tabs[str(num)])}"')

    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "get":
            ids_tabs = tabs[value]
            print(f"work in {len(ids_tabs)} cases")
    del tabs

    return ids_tabs
def main(ids_tab):
    printe.output(f"<<purple>> start.py all: {len(ids_tab)}:")
    # ---
    print_memory()
    # ---
    if "test" not in sys.argv and len(ids_tab) > 100:
        ids_tab = ddo(ids_tab)
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId = va["caseId"]
        case_url = va["url"]
        # ---
        author = va.get("author", "")
        # ---
        if not author:
            author = infos.get(case_url, {}).get(str(caseId), "")
        # ---
        if not author:
            author = authors.get(str(caseId), "")
        # ---
        title = va["title"]
        # ---
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        tab.append({"caseId": caseId, "case_url": case_url, "title": title, "studies": studies, "author": author})
    # ---
    del ids_tab
    # ---
    multi_work(tab)

def main_by_ids(ids):
    printe.output(f"<<purple>> start.py main_by_ids: {len(ids)=}:")
    # ---
    ids_tab = {caseId: all_ids[caseId] for caseId in ids if caseId in all_ids}
    # ---
    not_in = [c for c in ids if c not in all_ids]
    # ---
    print(f"main_by_ids caseId not in all_ids: {len(not_in)}")
    # ---
    main(ids_tab)

if __name__ == "__main__":
    # ---
    if "test" in sys.argv:
        ids_by_caseId = {"161846": {"url": "https://radiopaedia.org/cases/cholangiocarcinoma-25", "caseId": 161846, "title": "Cholangiocarcinoma", "studies": ["https://radiopaedia.org/cases/161846/studies/132257"], "author": "Mohammadtaghi Niknejad", "system": "Hepatobiliary", "published": "19 Feb 2023"}}
    # ---
    print("ids_by_caseId: ", len(ids_by_caseId))
    # ---
    main(ids_by_caseId)
