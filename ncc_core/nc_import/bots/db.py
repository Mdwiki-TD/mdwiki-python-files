'''

Usage:
# from nc_import.bots.db import add_to_db # add_to_db(title, code)

'''
# ---

import os
from newapi.db_bot import LiteDB

root_path = "/data/project/"

if os.path.exists("I:/"):
    root_path = "I:/"

db_path = f"{root_path}mdwiki/public_html/ncc/Tables/nc_files.db"

print(db_path)

nc_files_db = LiteDB(db_path)

def create():
    nc_files_db.create_table(
        "nc_files", 
        {"id": int, "lang": str, "title": str, "views": int, "dat": str}, 
        pk="id",
        defaults = {"views": 0},
        )

def add_to_db(title, code):
    data = {"lang": code, "title": title}

    nc_files_db.insert("nc_files", data)

if __name__ == "__main__":
    create()
    
    add_to_db("File:Chondrosarcoma_of_the_nasal_septum_(Radiopaedia_165701-135935_Sagittal_2).jpeg", "af")
    
    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)
