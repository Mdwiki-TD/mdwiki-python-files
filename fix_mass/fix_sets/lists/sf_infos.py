"""
python3 core8/pwb.py fix_mass/fix_sets/lists/sf_infos

from fix_mass.fix_sets.lists.sf_infos import from_sf_infs # from_sf_infs(url, study_id)

"""
import json
from newapi import printe

from fix_mass.fix_sets.jsons_dirs import jsons_dir

# ---
starts_with = "https://prod-images-static.radiopaedia.org/images"
# ---
sfinfs_file = jsons_dir / "sf_infos.json"
# ---
if not sfinfs_file.exists():
    sfinfs_file.write_text("{}")
# ---
sfs_infos = {}
# ---
with open(sfinfs_file, "r", encoding="utf-8") as f:
    sfs_infos = json.load(f)


def from_sf_infs(url, study_id):
    # ---
    if url.startswith(starts_with):
        url = url[len(starts_with) :]
    # ---
    lista = sfs_infos.get(url)
    # ---
    if not lista:
        printe.output(f"from_sf_infs: not found: {url}")
        return ""
    # ---
    if len(lista) == 1:
        return lista[0]
    # ---
    printe.output(f"from_sf_infs: {len(lista)}")
    # ---
    for file in lista:
        # File:Persistent trigeminal artery (Radiopaedia 56019-62643 Axial 14).jpg
        staa = f"-{study_id} "
        if staa in file:
            return file
    # ---
    printe.output(f"from_sf_infs: not found: {url}")
    # ---
    return ""
