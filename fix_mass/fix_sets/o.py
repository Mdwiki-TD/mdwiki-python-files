"""

python3 core8/pwb.py fix_mass/fix_sets/o reverse noapi
python3 core8/pwb.py fix_mass/fix_sets/o

tfj run seta1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/o noapi multi"
tfj run seta2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/o noapi multi reverse"

"""
import sys
from fix_mass.fix_sets.new import work_one_study

main_ids_text = """
    101212
    101577
    102511
    102597
    103211
    103490
    103613
    103754
    106274
    106710
    107853
    109737
    111634
    111699
    112160
    11332
    11443
    11444
    114596
    11471
    11536
    11603
    11640
    118562
    122237
    12525
    127355
    14090
    143304
    14341
    14883
    15349
    16124
    16202
    16204
    16907
    18427
    18516
    20060
    20387
    21758
    22171
    22172
    22211
    22452
    22453
    22457
    23288
    23448
    23962
    24543
    25938
    25970
    25971
    27442
    28573
    28574
    28746
    28776
    29667
    30185
    31126
    31929
    31930
    33692
    33806
    34173
    34334
    34491
    34492
    35061
    36137
    36806
    37268
    37289
    37297
    37298
    38978
    39393
    39444
    39445
    39446
    39664
    39817
    39944
    40047
    40137
    41372
    41796
    42322
    42470
    42477
    42478
    42753
    42757
    43041
    43044
    43048
    43052
    43791
    43813
    43814
    44527
    44876
    45394
    45397
    45435
    45436
    45691
    45704
    46196
    46262
    46263
    47387
    47388
    47479
    48162
    48532
    49016
    49179
    50456
    51088
    51089
    52383
    52749
    52795
    52796
    53177
    53179
    53180
    53564
    53755
    54084
    54296
    54297
    55108
    55341
    55631
    55632
    56978
    56980
    57086
    57113
    57114
    57598
    57599
    57870
    58325
    58487
    59492
    59966
    60613
    62069
    62100
    62101
    62429
    62430
    62570
    64226
    64341
    64342
    64368
    64369
    64436
    64509
    64510
    64511
    65078
    65079
    65256
    65257
    65258
    66136
    66140
    6645
    66596
    68031
    68737
    68783
    69578
    69633
    71164
    74282
    74283
    7471
    7472
    76611
    76635
    76636
    76637
    76638
    77935
    78450
    78451
    80157
    80188
    80302
    80303
    80304
    81216
    81527
    82361
    82921
    84195
    91342
    93901
    96427
    96433
    96434
    97305
    97753
    97760
    98545
    98798
    99259
    99632
"""
# ---
main_ids = [x.strip() for x in main_ids_text.split("\n") if x.strip()]

# split main_ids to 2 liist
main_ids1, main_ids2 = main_ids[: len(main_ids) // 2], main_ids[len(main_ids) // 2 :]

main_ids = main_ids1
main_ids.sort()

if "reverse" in sys.argv:
    main_ids = main_ids2
    main_ids.sort(reverse=True)

print(f"len main_ids: {len(main_ids)}")
# ---
for study_id in main_ids:
    work_one_study(study_id)
