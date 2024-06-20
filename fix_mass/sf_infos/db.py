"""
python3 core8/pwb.py fix_mass/sf_infos/db 54575469

from fix_mass.sf_infos.db import insert_url_file # insert_url_file(url, file)

"""
import sys
import re
from datetime import datetime
from pathlib import Path

from newapi.db_bot import LiteDB


Dir = Path(__file__).parent
db_path = Dir / "sf_infos.sqlite"
infos_db = LiteDB(db_path)

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
    infos_db.insert(
        "infos",
        data,
    )


def insert_url_file(url, file):
    return insert_infos({"url": url, "urlid": "", "file": file})


def insert_all_infos(data_list, prnt=True):
    # ---
    data_list = [fix_data(x) for x in data_list]
    # ---
    data_list = [x for x in data_list if x["urlid"]]
    # ---
    infos_db.insert_all("infos", data_list, prnt=prnt)


def insert(data):
    not_in = {k: v for k, v in data.items() if k not in table_keys["infos"]}
    # ---
    print(f"keys not in table: {not_in}")
    # ---
    data = {k: v for k, v in data.items() if k in table_keys["infos"]}
    # ---
    infos_db.insert(
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
    data = infos_db.select_or("infos", to_s)
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
            infos_db.update(sql)


def query(sql):
    return infos_db.query(sql)


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
            "urlid": "33264355",
            "file": "File:Postoperative lumbar nerve root enhancement (Radiopaedia 14096-13943 Sagittal 2).jpg",
        }
    )

    # Retrieve data
    data = infos_db.get_data("infos")
    for row in data:
        print(row)


def test2():
    print("________")

    # Retrieve data
    # data = infos_db.get_data("infos")
    # for row in data: print(row)
    # ---
    ids = [arg.strip() for arg in sys.argv if arg.isdigit()]
    # ---
    ids.extend([""])
    # ---
    for x in ids:
        data = infos_db.select("infos", {"urlid": x})
        # ---
        print(data)
    # ---
    print(infos_db.select("infos", {"url": ""}))


def test3():
    qua = """
    select * from infos
    where urlid = ""
    """

    # print(qua)
    # print(query(qua))
    # ---
    update_data(url="https://prod-images-static.radiopaedia.org/images/1159635/1159635.jpg", urlid="1159635", file="")


if __name__ == "__main__":
    if "test" in sys.argv:
        test()
    elif "test3" in sys.argv:
        test3()
    else:
        test2()
