import sys
from mass.radio.st3.start3 import main, ids_by_caseId
# --
aa = {}
for arg in sys.argv:
  arg, _, value = arg.partition(':')
  if arg.isdigit():
    ta = ids_by_caseId.get(arg) or ids_by_caseId.get(int(arg))
    if ta:
      aa[arg] = ta
#---
print(aa.keys())
main(aa)
