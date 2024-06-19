"""

python3 core8/pwb.py mass/radio/st3/oao
python3 core8/pwb.py mass/radio/st3/oao 33298

tfj run unyx1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/oao multi"
tfj run unyx2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/oao multi reverse"

tfj run oaoc1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/oao create multi"
tfj run oaoc2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3/oao create multi reverse"

"""
import re
import sys

sys.argv.append("del2")

from newapi import printe
from newapi.ncc_page import MainPage as ncc_MainPage, CatDepth
from mass.radio.jsons_files import jsons
from mass.radio.bots.add_cat import add_cat_to_images

cases_cats_list = jsons.cases_cats.copy()

main_ids_text = """
    10902
    11037
    11068
    11171
    11238
    11276
    12200
    14410
    14948
    154053
    15701
    16447
    16520
    17207
    178589
    18557
    18617
    20024
    20476
    21800
    22161
    22188
    22417
    22420
    23229
    23383
    23816
    24272
    25792
    25822
    27268
    28328
    28504
    28534
    29253
    29659
    30456
    31214
    32719
    32829
    33135
    33298
    33437
    33881
    34702
    35729
    35748
    35752
    37216
    37539
    37577
    37759
    37882
    37995
    38144
    39157
    39477
    39856
    39984
    40224
    40475
    41043
    41615
    41790
    42290
    42323
    42561
    42571
    42855
    42950
    43008
    43911
    43966
    4443
    4447
    44489
    44737
    45051
    45183
    46104
    46619
    47693
    47968
    47999
    48289
    48584
    48742
    49006
    49206
    49837
    50046
    50278
    51300
    51360
    51799
    52019
    52574
    53486
    53862
    54389
    55572
    55596
    55844
    55955
    57288
    57395
    57421
    57481
    57552
    58043
    58182
    58904
    59255
    5930
    60362
    60929
    60964
    61599
    62812
    65260
    67253
    67273
    68401
    68741
    70122
    70242
    71000
    71226
    71910
    72391
    73389
    78588
    82339
    82959
    83338
    83345
    83455
    83667
    84030
    84330
    85517
    85725
    85766
    86524
    86986
    87214
    87318
    87426
    89348
    90499
    91916
    93330
    93383
    93705
    95353
    98093
"""


def create_sub_cat(study_id, case_id, case_cat, title):
    text = f"* [https://radiopaedia.org/cases/{case_id}/studies/{study_id} study: {study_id}]\n"
    text += f"[[{case_cat}|*]]\n"
    text += f"[[Category:Radiopaedia studies|{study_id}]]\n"
    # ---
    printe.output(f"<<yellow>> create_sub_cat: {title}")
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    if page.exists():
        return True
    # ---
    create = page.Create(text=text, summary="")
    # ---
    if create:
        return True
    # ---
    return False


def filter_members(cat_members):
    data = {}
    # ---
    not_match = 0
    # ---
    for x in cat_members:
        # ---
        if not x.startswith("File:"):
            # printe.output(f"!{x}")
            continue
        # ---
        # search for (Radiopaedia \d+-\d+
        se = re.match(r".*?\(Radiopaedia \d+-(\d+)", x)
        # ---
        if not se:
            printe.output(f"!{x}")
            not_match += 1
            continue
        # ---
        study_id = se.group(1)
        # ---
        if study_id not in data:
            data[study_id] = []
        # ---
        data[study_id].append(x)
    # ---
    return data


def get_ids():
    main_ids = [x.strip() for x in main_ids_text.split("\n") if x.strip()]

    # split main_ids to 2 liist
    main_ids1, main_ids2 = main_ids[: len(main_ids) // 2], main_ids[len(main_ids) // 2 :]

    main_ids = main_ids1
    main_ids.sort()

    if "reverse" in sys.argv:
        main_ids = main_ids2
        main_ids.sort(reverse=True)

    return main_ids


def start(ids):
    da = []
    # ---
    if not ids:
        ids = get_ids()
    # ---
    for case_id in ids:
        cat = cases_cats_list.get(case_id)
        # ---
        if not cat:
            printe.output(f"!{case_id} not found")
            continue
        # ---
        cat_members = CatDepth(cat, sitecode="www", family="nccommons", depth=0)
        # ---
        sub_cat = [x for x in cat_members if x.startswith("Category:")]
        # ---
        cat2 = cat.replace(f" {case_id}", "")
        # ---
        print(sub_cat)
        # ---
        filterd = filter_members(cat_members)
        # ---
        for x, files in filterd.items():
            # ---
            set_cat = f"{cat2} id: {case_id} study: {x}"
            # ---
            in_subs = set_cat in sub_cat
            # ---
            printe.output(f"  {x}, {len(files)=}, {set_cat}, {in_subs}")
            # ---
            if "create" in sys.argv:
                if not in_subs:
                    in_subs = create_sub_cat(x, case_id, cat, set_cat)
                    if in_subs:
                        # add_cat_to_images(files, set_cat, cat)
                        da.append((files, set_cat, cat))
            else:
                # ---
                if not in_subs:
                    continue
                # ---
                # add_cat_to_images(files, set_cat, cat)
                da.append((files, set_cat, cat))
    # ---
    printe.output(f"len da: {len(da)}")
    printe.output(f"len da: {len(da)}")
    printe.output(f"len da: {len(da)}")
    printe.output(f"len da: {len(da)}")
    # ---
    for files, set_cat, cat in da:
        add_cat_to_images(files, set_cat, cat)


if __name__ == "__main__":
    # ---
    ids2 = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    start(ids2)
