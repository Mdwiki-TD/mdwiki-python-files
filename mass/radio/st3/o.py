"""
python3 core8/pwb.py mass/radio/st3/o 11171
"""
import sys
from mass.radio.st3.start3 import ids_by_caseId, main

# Parsing arguments
lookup_dict = {}
for arg in sys.argv[1:]:
    arg, _, value = arg.partition(':')
    if arg.isdigit():
        case_id = int(arg)
        ta = ids_by_caseId.get(case_id) or ids_by_caseId.get(arg)
        if ta:
            lookup_dict[case_id] = ta

# Printing keys and calling main
print(list(lookup_dict.keys()))
main(lookup_dict)
