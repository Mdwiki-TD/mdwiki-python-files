"""

from fix_mass.helps_bot.file_bot import from_cach, dumpit

"""
import sys
import json
from pathlib import Path
from newapi import printe


def from_cach(file):
    if "nocach" in sys.argv:
        return {}
    file = Path(file)
    if file.exists():
        try:
            return json.loads(file.read_text())
        except Exception as e:
            printe.output(f"<<red>> from_cach: {file} error: {e}")
    return {}


def dumpit(data, file):
    file = Path(file)
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            printe.output(f"<<green>> write {len(data)} to file: {file}")

    except Exception as e:
        printe.output(f"<<red>> Error writing to file {file}: {str(e)}")
