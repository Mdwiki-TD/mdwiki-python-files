"""

python3 core8/pwb.py z/labels

"""

import json
# from newapi.page import NEW_API
from tqdm import tqdm
from newapi.page import MainPage
# from newapi.wd_sparql import get_query_result
from pathlib import Path
import csv

from newapi.api_utils import wd_sparql
from himo_api.himoAPI import wdapi_new

Dir = Path(__file__).parent

# api = NEW_API('en', family='wikipedia')
# api.Login_to_wiki()

qids_file = Dir / "qids.json"

data = json.loads()
