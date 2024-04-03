'''

Usage:
# from nc_import.bots.db import add_to_db

'''
# ---

import os
import sqlite_utils
from datetime import datetime

def tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))

class NCFilesDB:
    def __init__(self, db_path):
        self.db_path = db_path
        # self.db = sqlite_utils.Database(db_path, tracer=tracer)
        self.db = sqlite_utils.Database(db_path)

    def create_table(self, table_name, fields, pk="id", **kwargs):
        # Create table if it doesn't exist
        self.db[table_name].create(fields, pk=pk, if_not_exists=True, ignore=True, **kwargs)

    def show_tables(self):
        tabs = self.db.table_names()
        for tab in tabs:
            print(f"Table: {tab}")
            print(f"schema: {self.db[tab].schema}")

    def insert(self, table_name, data, check=True):
        if check:
            is_in = self.select("nc_files", data)
            if is_in:
                print(f" Skipping {data} - already in database")
                return
        
        self.db[table_name].insert(data, ignore=True, pk="id")

    def get_data(self, table_name):
        return self.db[table_name].rows

    def select(self, table_name, args):
        where = " and ".join([f"{k} = '{v}'" for k, v in args.items()])
        lista = []
        for row in self.db[table_name].rows_where(where):
            lista.append(row)
        return lista


def add_to_db(title, code):
    db_path = "/data/mdwiki/public_html/ncc/Tables/nc_files.db"
    if not os.path.exists(db_path):
        db_path = "I:/mdwiki/pybot/ncc_core/nc_import/bots/nc_files.db"
        
    nc_files_db = NCFilesDB(db_path)

    data = {"lang": code, "title": title}

    nc_files_db.insert("nc_files", data)
    

def test():
    db_path = "/data/mdwiki/public_html/ncc/Tables/nc_files.db"
    if not os.path.exists(db_path):
        db_path = "I:/mdwiki/pybot/ncc_core/nc_import/bots/nc_files.db"
        
    nc_files_db = NCFilesDB(db_path)

    nc_files_db.create_table(
        "nc_files", 
        {"id": int, "lang": str, "title": str, "views": int, "dat": str}, 
        pk="id",
        defaults = {"views": 0},
        )

    nc_files_db.show_tables()

    # Insert sample data
    nc_files_db.insert("nc_files", {
        "lang": "English",
        "title": "Sample Title 1",
        # "views": 100,
        "dat": datetime.now().strftime("%Y-%m-%d")
    })

    nc_files_db.insert("nc_files", {
        "lang": "French",
        "title": "Sample Title 2",
        # "views": 200,
        "dat": datetime.now().strftime("%Y-%m-%d")
    })

    # Retrieve data
    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)
    
def test2():
    db_path = "/data/mdwiki/public_html/ncc/Tables/nc_files.db"
    if not os.path.exists(db_path):
        db_path = "I:/mdwiki/pybot/ncc_core/nc_import/bots/nc_files.db"
        
    nc_files_db = NCFilesDB(db_path)

    print("________")
    # Select data
    # data = nc_files_db.select("nc_files", {"lang": "English"})
    # print(data)
    # for row in data:
    #     print(row)

    # Retrieve data
    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)
    
if __name__ == "__main__":
    test()
    add_to_db("File:xx", "oxr")
    test2()