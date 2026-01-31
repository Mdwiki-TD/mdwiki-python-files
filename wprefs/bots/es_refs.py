"""
python3 core8/pwb.py wprefs/bots/es_refs
"""

import wikitextparser as wtp
from pathlib import Path


def make_line(refs):
    line = "\n"
    # ---
    for g, gag in refs.items():
        # ---
        for name, ref in gag.items():
            la = f'<ref name="{name}">{ref}</ref>\n'
            if g != "":
                la = f'<ref group="{g}" name="{name}">{ref}</ref>\n'
            # ---
            line += la
    # ---
    line = line.strip()
    # ---
    return line


def get_refs(text):
    # ---
    parsed = wtp.parse(text)
    tags = parsed.get_tags()
    # ---
    numb = 0
    refs = {}
    # ---
    refs_to_name = {}
    # ---
    for x in tags:
        # ---
        if not x or not x.name:
            continue
        if x.name != "ref":
            continue
        if not x.contents:
            continue
        # ---
        conts = x.contents.strip()
        # ---
        attrs = x.attrs
        # ---
        name = refs_to_name.get(conts) or attrs.get("name", "").strip()
        # ---
        group = attrs.get("group", "").strip()
        # ---
        if group not in refs:
            refs[group] = {}
        # ---
        if not name:
            numb += 1
            name = f"autogen_{numb}"
            x.set_attr("name", name)
        # ---
        if name not in refs[group]:
            refs[group][name] = x.contents
        # elif refs[group][name] != x.contents:
        #     print(f"x.contents = {x.contents}")
        # ---
        refs_to_name[conts] = name
        # ---
        asas = f'<ref name="{name}" />'
        if group != "":
            asas = f'<ref group="{group}" name="{name}" />'
        # ---
        x.string = asas
    # ---
    new_text = parsed.string
    # ---
    return refs, new_text


def add_line_to_temp(line, new_text):
    # ---
    parsed = wtp.parse(new_text)
    # ---
    for template in reversed(parsed.templates):
        # ---
        if not template:
            continue
        # ---
        template_name = str(template.normal_name()).strip()
        # ---
        if template_name.lower() not in ["reflist", "listaref"]:
            continue
        # ---
        refs_arg = template.get_arg("refs")
        # ---
        if refs_arg and refs_arg.value and refs_arg.value.strip():
            line = f"{refs_arg.value.strip():}\n{line.strip()}"
        # ---
        template.set_arg("refs", f"\n{line}")
        # ---
        new_text = parsed.string
        # ---
        return new_text
    # ---
    return new_text


def mv_es_refs(text):
    # ---
    refs, new_text = get_refs(text)
    # ---
    line = make_line(refs)
    # ---
    new_text = add_line_to_temp(line, new_text)
    # ---
    if new_text.find(line.strip()) == -1:
        return text
    # ---
    return new_text


if __name__ == "__main__":
    file = Path(__file__).parent / "es_mv.txt"
    # ---
    text = file.read_text(encoding="utf-8")
    # ---
    new_text = mv_es_refs(text)
    # ---
    file2 = Path(__file__).parent / "es_mv_fixed.txt"
    # ---
    file2.write_text(new_text, encoding="utf-8")
