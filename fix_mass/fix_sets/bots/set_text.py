"""

from fix_mass.fix_sets.bots.set_text import make_text_one_study


"""


def make_text(modality, files, set_title):
    # ---
    text = f"== {modality} ==\n"

    text += "{{Imagestack\n|width=850\n"
    text += f"|title={set_title}\n|align=centre\n|loop=no\n"

    # sort files {1: "file:...", 2: "file:..."}
    files = {k: v for k, v in sorted(files.items())}

    for n, image_name in files.items():
        text += f"|{image_name}|\n"
    # ---
    text += "\n}}\n\n"
    # ---
    return text


def make_text_one_study(json_data, url_to_file, study_title):
    # ---
    text = ""
    # ---
    to_move = {}
    # ---
    for x in json_data:
        # ---
        noo = 0
        # ---
        print(x.keys())
        # ---
        modality = x["modality"]
        images = x["images"]
        # ---
        files = {}
        # ---
        # sort images by position key
        images = sorted(images, key=lambda x: x["position"])
        # ---
        for n, image in enumerate(images, start=1):
            # ---
            public_filename = image["public_filename"]
            # ---
            file_name = url_to_file.get(public_filename)
            # ---
            if not file_name:
                noo += 1
                file_name = public_filename
            # ---
            files[n] = file_name
            # ---
        # ---
        print(f"noo: {noo}")
        print(f"files: {len(files)}")
        # ---
        text += make_text(modality, files, study_title)
        # ---
        to_move[modality] = files
        # ---
    # ---
    return text, to_move
