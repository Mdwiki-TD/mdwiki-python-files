"""

python3 core8/pwb.py newupdater/tests/test_med
python3 I:/mdwiki/pybot/newupdater/tests/test_med.py Retinol

"""

import os
import sys

os.environ["DEBUGNEW"] = "true"

from pathlib import Path


if Dir := Path(__file__).parent.parent:
    sys.path.append(str(Dir))


title = sys.argv[1] if len(sys.argv) > 1 else "Retinol"
# ---
command1 = f"python3 I:/mdwiki/pybot/newupdater/med.py {title} from_toolforge xx"
# ---
command2 = f"python3 I:/mdwiki/pybot/newupdater/med.py {title} from_toolforge xx"
# ---
print(f"command1: {command1}")
ux = os.system(command1)
# ---
print(f"result1: {ux}")
# ---
print(f"command2: {command2}")
uu = os.system(command2)
# ---
print(f"result2: {uu}")
# ---
