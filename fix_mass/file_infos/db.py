"""
python3 core8/pwb.py fix_mass/file_infos/db test3

from fix_mass.file_infos.db import find_data # find_data(url="", urlid="", file="")
from fix_mass.file_infos.db import insert_all_infos # insert_all_infos(data_list, prnt=True)
from fix_mass.file_infos.db import insert_url_file # insert_url_file(url, file)

"""
import sys
import re
from pathlib import Path

from newapi.db_bot import LiteDB

Dir = Path(__file__).parent
db_path = Dir / "db.sqlite"
files_db = LiteDB(db_path)

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


def insert_infos(data):
    # ---
    data = fix_data(data)
    # ---
    files_db.insert(
        "infos",
        data,
    )


def insert_url_file(url, file):
    return insert_infos({"url": url, "urlid": "", "file": file})


def insert_all_infos(data_list_or, prnt=True):
    # ---
    data_list = [fix_data(x) for x in data_list_or]
    # ---
    data_list = [x for x in data_list if x["urlid"]]
    # ---
    print(f"insert_all_infos: data_list_or: {len(data_list_or)}, with 'urlid': {len(data_list)} ")
    # ---
    files_db.insert_all("infos", data_list, prnt=prnt)
    # ---
    del data_list, data_list_or


def insert(data):
    not_in = {k: v for k, v in data.items() if k not in table_keys["infos"]}
    # ---
    print(f"keys not in table: {not_in}")
    # ---
    data = {k: v for k, v in data.items() if k in table_keys["infos"]}
    # ---
    files_db.insert(
        "infos",
        data,
    )


def find_data(url="", urlid="", file=""):
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
    data = files_db.select_or("infos", to_s)
    return data


def update_data(url="", urlid="", file=""):
    data_in = find_data(url, urlid, file)
    # ---
    if not data_in:
        return insert_infos({"url": url, "urlid": urlid, "file": file})
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
            files_db.update(sql)
    # ---
    del new_data, data_in


def query(sql):
    return files_db.query(sql)


def test():
    # Insert sample data
    insert(
        {
            "url": "https://prod-images-static.radiopaedia.org/images/33333333/xxxxxxxxxxx.JPG",
            "urlid": "33333333",
            "file": "",
        }
    )
    insert(
        {
            "url": "",
            "urlid": "020202",
            "file": "File:tests.jpg",
        }
    )

    # Retrieve data
    data = files_db.get_data("infos")
    for row in data:
        print(row)


def test2():
    print("________")

    # Retrieve data
    # data = files_db.get_data("infos")
    # for row in data: print(row)
    # ---
    ids = [arg.strip() for arg in sys.argv if arg.isdigit()]
    # ---
    ids.extend([""])
    # ---
    for x in ids:
        data = files_db.select("infos", {"urlid": x})
        # ---
        print(data)
    # ---
    print(files_db.select("infos", {"url": ""}))


def test3():
    qua = "SELECT * from infos"
    # ---
    print(qua)
    # ---
    result = query(qua)
    # ---
    print(f"len result: {len(result)}")
    # ---
    if "printall" in sys.argv:
        for row in result:
            print(row)


def check():
    files_db.create_table(
        "infos",
        {"id": int, "url": str, "urlid": str, "file": str},
        pk="id",
        defaults={
            "url": "",
            "file": "",
            "urlid": "",
        },
    )

if __name__ == "__main__":
    check()
    if "test" in sys.argv:
        test()
    elif "test3" in sys.argv:
        test3()
    else:
        test2()
