"""

from fix_mass.fix_sets.bots.set_text import make_text_one_study
from fix_mass.fix_sets.bots.done import studies_done_append

"""
from newapi import printe
from fix_mass.fix_sets.bots.has_url import has_url_append
from fix_mass.fix_sets.bots.find_from_url import find_file_name_from_url
from fix_mass.fix_sets.lists.sf_infos import from_sf_infos  # from_sf_infos(url, study_id)


def make_text_one_study(json_data, data, study_title, study_id):
    # ---
    url_to_file = {v["img_url"]: x for x, v in data.items()}
    # ---
    to_move = {}
    # ---
    modalities = set([x["modality"] for x in json_data])
    # ---
    printe.output(f"modalities: {modalities}")
    # ---
    noo = 0
    # ---
    urlls = {}
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
            plane_projection = image["plane_projection"]
            aux_modality = image["aux_modality"]
            # ---
            # if len(modalities) == 1 and plane_projection:
            ty = plane_projection
            # ---
            if aux_modality:
                ty = f"{plane_projection} {aux_modality}"
            # ---
            if ty not in texts:
                texts[ty] = ""
            # ---
            if ty not in to_move:
                to_move[ty] = {}
            # ---
            public_filename = image["public_filename"]
            # ---
            texts[ty] += f"|{public_filename}|\n"
            # ---
            file_name = ""
            # ---
            # file_name = url_to_file.get(public_filename)
            # # ---
            # if not file_name:
            #     file_name = from_sf_infos(public_filename, study_id)
            # ---
            if not file_name:
                file_name = find_file_name_from_url(public_filename)
            # ---
            if file_name and not file_name.startswith("File:"):
                file_name = "File:" + file_name
            # ---
            if file_name:
                urlls[public_filename] = file_name
            else:
                noo += 1
                file_name = public_filename
            # ---
            numb = len(to_move[ty]) + 1
            # ---
            to_move[ty][numb] = file_name
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
    if all_files == len(to_move):
        printe.output("len to_move == all_files")
        has_url_append(study_id)
        return text, to_move
    # ---
    for ty, files in to_move.items():
        # ---
        print(f"ty: {ty}, files: {len(files)}")
        # ---
        text += f"== {ty} ==\n"
        text += "{{Imagestack\n|width=850\n"
        text += f"|title={study_title2}\n|align=centre\n|loop=no\n"
        text += texts[ty].strip()
        text += "\n}}\n"
        # ---
    # ---
    return text, to_move
