"""

from fix_mass.fix_sets.bots.set_text2 import make_text_study
"""
import sys
from newapi import printe
from fix_mass.fix_sets.bots.has_url import has_url_append
from fix_mass.fix_sets.bots2.files_names_bot import get_files_names


def make_text_study(json_data, data, study_title, study_id):
    # ---
    url_to_file = {v["img_url"]: x for x, v in data.items()}
    # ---
    maain_uurls = []
    # ---
    for x in json_data:
        maain_uurls.extend([x["public_filename"] for x in x["images"]])
    # ---
    maain_uurls = list(set(maain_uurls))
    # ---
    files_names = get_files_names(maain_uurls, url_to_file, study_id)
    # ---
    modalities = set([x["modality"] for x in json_data])
    # ---
    printe.output(f"modalities: {modalities}")
    # ---
    noo = 0
    # ---
    urlls = {}
    # ---
    to_move = {}
    # ---
    texts = {}
    # ---
    for x in json_data:
        # ---
        modality = x["modality"]
        images = x["images"]
        # ---
        ty = modality
        # ---
        # print(f"modality: {modality}, images: {len(images)}")
        # ---
        # sort images by position key
        images = sorted(images, key=lambda x: x["position"])
        # ---
        for _n, image in enumerate(images, start=1):
            # ---
            plane_projection = image["plane_projection"] or modality or ""
            aux_modality = image["aux_modality"] or ""
            # ---
            # if len(modalities) == 1 and plane_projection:
            ty = plane_projection
            # ---
            if aux_modality:
                ty = f"{plane_projection} {aux_modality}"
            # ---
            ty = ty.strip()
            # ---
            if not ty:
                ty = ""
            # ---
            if ty not in texts:
                texts[ty] = ""
            # ---
            if ty not in to_move:
                to_move[ty] = {}
            # ---
            url = image["public_filename"]
            # ---
            texts[ty] += f"|{url}|\n"
            # ---
            file_name = files_names.get(url)
            # ---
            if file_name:
                urlls[url] = file_name
            else:
                noo += 1
                file_name = url
            # ---
            to_move[ty][len(to_move[ty]) + 1] = file_name
    # ---
    print(f"noo: {noo}")
    # ---
    text = ""
    # ---
    study_title2 = study_title
    # ---
    for ty, txt in texts.copy().items():
        for url, file_name in urlls.items():
            txt = txt.replace(url, file_name)
        # ---
        texts[ty] = txt
    # ---
    # sum all files in to_move
    all_files = sum([len(x) for x in to_move.values()])
    # ---
    if all_files == len(to_move) and all_files > 3:
        printe.output("len to_move == all_files")
        has_url_append(study_id)
        return text, to_move
    # ---
    for ty, files in to_move.items():
        # ---
        print(f"ty: {ty}, files: {len(files)}")
        # ---
        if ty.strip():
            text += f"== {ty} ==\n"
        text += "{{Imagestack\n|width=850\n"
        text += f"|title={study_title2}\n|align=centre\n|loop=no\n"
        text += texts[ty].strip()
        text += "\n}}\n"
    # ---
    return text, to_move
