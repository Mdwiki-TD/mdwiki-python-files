"""
s
from fix_mass.fix_sets.bots.mv_files import to_move_work

"""
import re
import json
import sys
from pathlib import Path
from newapi import printe
from newapi.ncc_page import CatDepth

Dir = Path(__file__).parent.parent

st_dit = Dir / "jsons/studies_files"

from fix_mass.fix_sets.jsons.files import studies_titles, study_to_case_cats


def dump_it(data):
    for s_id, files in data.items():
        with open(st_dit / f"{s_id}.json", "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
            printe.output(f"<<green>> write {len(files)} to {s_id}.json")

def change_names(file_dict):
    # قاموس جديد لتخزين الأسماء المعدلة
    modified_file_dict = {}

    # تكون أسماء الملفات مطابقة للمفاتيح
    for key, value in file_dict.items():
        # تحويل الرقم إلى سلسلة نصية وإضافة صفر إذا كان الرقم أحادي الخانة
        # new_key = '{:02d}'.format(key)
        new_key = f'0{key}'
        # استبدال الرقم في الجزء الأخير من اسم الملف
        new_filename = value.replace(value[value.rfind(' ')+1:value.find(').jpg')], new_key)
        # إضافة الاسم المعدل إلى القاموس الجديد
        modified_file_dict[value] = new_filename
    
    return modified_file_dict
def to_move_work(text, to_move):
    # ---
    new_text = text
    # ---
    for ty, files in to_move.items():
        # ---
        printe.output(f"<<blue>> {ty} {len(files)}")
        # printe.output(files)
        # ---
        neww = change_names(files)
        # ---
        printe.output(json.dumps(neww, indent=2))
        # ---
    # ---
    return text
