"""

python3 core8/pwb.py fix_mass/dp_infos/me

"""
import tqdm
import sqlite3
from pathlib import Path
from newapi import printe

# Define database paths
Dir = Path(__file__).parent
path_db_1 = Dir / "fs_infos_duplict.sqlite"
path_db_2 = Dir / "fs_infos_duplict1.sqlite"
db_path_new = Dir / "fs_infos_duplict_new.sqlite"

# Create and connect to new database
conn_new = sqlite3.connect(db_path_new)
cursor_new = conn_new.cursor()

# Create table in new database
printe.output("<<yellow>> Create table in new database.")
cursor_new.execute(
    """
    CREATE TABLE IF NOT EXISTS infos (
        id INTEGER PRIMARY KEY,
        url TEXT,
        urlid TEXT,
        file TEXT
    )"""
)

# Open connections to old databases
conn_1 = sqlite3.connect(path_db_1)
conn_2 = sqlite3.connect(path_db_2)
cursor_1 = conn_1.cursor()
cursor_2 = conn_2.cursor()

# Fetch data from first database
printe.output("<<yellow>> Fetch data from first database.")
cursor_1.execute("SELECT url, urlid, file FROM infos")

rows_1 = cursor_1.fetchall()
db_1_lenth = len(rows_1)

# Fetch data from second database
printe.output("<<yellow>> Fetch data from second database.")

conn_1.close()
cursor_2.execute("SELECT url, urlid, file FROM infos")

rows_2 = cursor_2.fetchall()
db_2_lenth = len(rows_2)

conn_2.close()

printe.output("<<yellow>> merge data from both databases without duplicates.")

new_data = set(rows_1).union(set(rows_2))

new_data = set(new_data)

db_new_lenth = len(new_data)

# Insert data into new database
printe.output("<<yellow>> Insert data into new database.")

for row in tqdm.tqdm(new_data):
    cursor_new.execute("INSERT OR IGNORE INTO infos (url, urlid, file) VALUES (?, ?, ?)", row)

# Commit changes and close connections
printe.output("<<yellow>> Commit changes and close connections.")

conn_new.commit()

# len of data in new db
cursor_new.execute("SELECT * FROM infos")
data_new = cursor_new.fetchall()
db_new_lenth_in = len(data_new)

conn_new.close()

print(f"db_1_lenth: {db_1_lenth:,}")
print(f"db_2_lenth: {db_2_lenth:,}")
print(f"db_new_lenth: {db_new_lenth:,}")
print(f"db_new_lenth_in: {db_new_lenth_in:,}")
