"""
python3 core8/pwb.py fix_mass/sqlite_bot

from fix_mass.sqlite_bot import SqlLiteFilesDB
db = SqlLiteFilesDB("db.sqlite")

"""
import sys
import re

from newapi.db_bot import LiteDB

table_keys = {
    "infos": ["url", "urlid", "file"],
}


def fix_data(data):
    # ---
    if data["url"].startswith("/"):
        data["url"] = f"https://prod-images-static.radiopaedia.org/images{data['url']}"
    # ---
    urlid = data.get("urlid")
    # ---
    if not urlid and data["url"]:
        # match https://prod-images-static.radiopaedia.org/images/(\d+)/
        ma = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/", data["url"])
        if ma:
            urlid = ma.group(1)
    # ---
    return {
        "url": data["url"],
        "urlid": urlid,
        "file": data["file"],
    }


class SqlLiteFilesDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.main_db = LiteDB(db_path)
        self.check()

    def insert_infos(self, data):
        # ---
        data = fix_data(data)
        # ---
        self.main_db.insert(
            "infos",
            data,
        )

    def insert_url_file(self, url, file):
        return self.insert_infos({"url": url, "urlid": "", "file": file})

    def insert_all_infos(self, data_list_or, prnt=True):
        # ---
        data_list = [fix_data(x) for x in data_list_or]
        # ---
        data_list = [x for x in data_list if x["urlid"]]
        # ---
        print(f"insert_all_infos: data_list_or: {len(data_list_or)}, with 'urlid': {len(data_list)} ")
        # ---
        self.main_db.insert_all("infos", data_list, prnt=prnt)
        # ---
        del data_list, data_list_or

    def insert(self, data):
        not_in = {k: v for k, v in data.items() if k not in table_keys["infos"]}
        # ---
        print(f"keys not in table: {not_in}")
        # ---
        data = {k: v for k, v in data.items() if k in table_keys["infos"]}
        # ---
        self.main_db.insert(
            "infos",
            data,
        )

    def find_data(self, url="", urlid="", file=""):
        to_s = {}
        # ---
        if url:
            to_s["url"] = url
        if urlid:
            to_s["urlid"] = urlid
        if file:
            to_s["file"] = file
        # ---
        if not to_s:
            return []
        # ---
        data = self.main_db.select_or("infos", to_s)
        return data

    def update_data(self, url="", urlid="", file=""):
        data_in = self.find_data(url, urlid, file)
        # ---
        if not data_in:
            return self.insert_infos({"url": url, "urlid": urlid, "file": file})
        # ---
        new_data = {"url": url, "urlid": urlid, "file": file}
        # ---
        print("data_in:")
        for x in data_in:
            print(x)
        # ---
        for row in data_in:
            # ---
            row2 = {}
            # ---
            for x, v in new_data.items():
                if v and not row[x]:
                    row2[x] = v
            # ---
            row_id = row["id"]
            # ---
            if row2:
                # ---
                sets = ", ".join([f"{k} = '{v}'" for k, v in row2.items()])
                # ---
                sql = f"update infos set {sets} where id = '{row_id}'"
                # ---
                print(sql)
                # ---
                self.main_db.update(sql)
        # ---
        del new_data, data_in

    def query(self, sql):
        return self.main_db.query(sql)

    def find_from_data_db(self, url, urlid):
        # ---
        if "nodb" in sys.argv:
            return ""
        # ---
        data = self.find_data(url=url, urlid=urlid, file="")
        # ---
        if not data:
            return ""
        # ---
        if len(data) == 1:
            return data[0]["file"]
        # ---
        for d in data:
            if d["url"] == url and d["file"]:
                return d["file"]
        # ---
        return ""

    def check(self):
        self.main_db.create_table(
            "infos",
            {"id": int, "url": str, "urlid": str, "file": str},
            pk="id",
            defaults={
                "url": "",
                "file": "",
                "urlid": "",
            },
        )

    def get_data(self, table_name="infos"):
        return self.main_db.get_data(table_name)

    def select(self, data, table_name="infos"):
        return self.main_db.select(table_name, data)
