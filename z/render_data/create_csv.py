"""
python3 I:/mdwiki/pybot/z/render_data/create_csv.py
"""
import re
import json
from pathlib import Path
import csv

Dir = Path(__file__).parent.parent

data_file = Dir / "csv.json"
data_duplicate_file = Dir / "csv_dup.json"
csv_file = Dir / "dictionary(ocr_resolved).csv"

data = []
duplicate_data = []
seen = {}  # key -> index in data


def same_dzongkha(a, b):
    """تأكد إذا كانت label و description متطابقة في الصفين"""
    return (
        (a.get("label") or "").strip() == (b.get("label") or "").strip()
        and (a.get("description") or "").strip() == (b.get("description") or "").strip()
    )


with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        en = row.get("\ufeffEnglish Term") or row.get("English Term")
        if row.get("\ufeffEnglish Term"):
            del row["\ufeffEnglish Term"]
        if row.get("English Term"):
            del row["English Term"]

        row["en"] = en
        key = en.lower().strip() if en else ""

        row = {k.strip() : re.sub(r'\s+', ' ', v).strip() for k, v in row.items()}

        if key in seen:
            original_index = seen[key]
            original_row = data[original_index]

            # تحقق من تطابق label و description
            if not same_dzongkha(original_row, row):
                # إذا لم يتم نقل الأصل سابقًا → انقله
                if original_index is not None:
                    duplicate_data.append(original_row)
                    seen[key] = None  # منع تكرار النقل
                duplicate_data.append(row)
        else:
            seen[key] = len(data)
            data.append(row)

# إزالة العناصر التي تم نقلها إلى المكررات
data = [row for i, row in enumerate(data)
        if i not in [idx for idx in seen.values() if idx is None]]

# فرز القوائم
data = sorted(data, key=lambda x: (x["en"] or "").lower().strip())
duplicate_data = sorted(duplicate_data, key=lambda x: (x["en"] or "").lower().strip())

with open(data_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

with open(data_duplicate_file, 'w', encoding='utf-8') as file:
    json.dump(duplicate_data, file, ensure_ascii=False, indent=4)

print(f"data: {len(data)}")
print(f"duplicate_data: {len(duplicate_data)}")
