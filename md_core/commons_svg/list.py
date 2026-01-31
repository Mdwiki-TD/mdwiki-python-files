# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

import mwclient
import wikitextparser as wtp

# --- Connect to Commons ---
site = mwclient.Site("commons.wikimedia.org")


def save_page(page_name, content):
    # Uncomment next line when ready to write
    # site.pages[page_name].save(content, summary="Update SVGLanguages entries")
    print(f"Would update {page_name} with {len(svg_map)} entries")
    with open(Path(__file__).parent / "list.wiki", "w", encoding="utf-8") as f:
        f.write(content)


# --- Load the template-to-file mapping ---
with open(Path(__file__).parent / "svg_languages.json", "r", encoding="utf-8") as f:
    svg_map = json.load(f)

# --- Target page ---
PAGE_NAME = "Commons:List of interactive data graphics"
page = site.pages[PAGE_NAME]
text = page.text()

# --- Split lines to edit ---
lines = text.splitlines()
updated_lines = []

# Regex to match OWID templates in bullet list
RE_TEMPLATE = re.compile(r"\*\[\[Template:([^|\]]+)")
RE_SVGLANG = re.compile(r"\{\{\s*SVGLanguages\s*\|[^}]*\}\}", re.I)

for line in lines:
    m = RE_TEMPLATE.search(line)
    if not m:
        updated_lines.append(line)
        continue

    template_name = m.group(1).strip()
    filename = svg_map.get(f"Template:{template_name}")

    if not filename:
        updated_lines.append(line)
        continue

    new_svg = f"{{{{SVGLanguages|{filename}}}}}"

    if RE_SVGLANG.search(line):
        # Replace old SVGLanguages
        line = RE_SVGLANG.sub(new_svg, line)
    else:
        # Append if missing
        line = line.rstrip() + "  " + new_svg

    updated_lines.append(line)

# --- Combine final text ---
new_text = "\n".join(updated_lines)

# --- Save function placeholder ---

save_page(PAGE_NAME, new_text)
