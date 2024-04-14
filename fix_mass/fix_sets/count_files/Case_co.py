"""
from fix_mass.radio.st3sort.count_files.Case_co import CaseDo
"""
import sys
import os
from pathlib import Path
import json
import traceback

# ---
from newapi import printe
from fix_mass.radio.get_studies import get_images_stacks, get_images
from fix_mass.radio.bots.studies_utf import dump_studies_urls_to_files

# ---
try:
    import pywikibot

    pywikibotoutput = pywikibot.output
except ImportError:
    pywikibotoutput = print
# ---
main_dir = Path(__file__).parent.parent
# ---
studies_dir = Path("/data/project/mdwiki/studies")
# ---
if not os.path.exists(studies_dir):
    printe.output(f"<<red>> studies_dir {studies_dir} not found")
    studies_dir = main_dir / "studies"
    printe.output(f"<<red>> studies_dir set to {studies_dir}")


def printt(s):
    if "nopr" in sys.argv:
        return
    printe.output(s)


class CaseDo:
    def __init__(self, caseId, title, studies_ids):
        self.caseId = caseId
        self.title = title
        self.studies_ids = studies_ids
        self.img_to_url = {}
        self.studies = {}
        self.category = f"Category:Radiopaedia case {self.caseId} {self.title}"
        # ---

    def get_studies(self):
        for study in self.studies_ids:
            st_file = studies_dir / f"{study}.json"
            # ---
            images = {}
            # ---
            if os.path.exists(st_file):
                try:
                    with open(st_file, encoding="utf-8") as f:
                        images = json.loads(f.read())
                except Exception as e:
                    print("<<lightred>> Traceback (most recent call last):")
                    printt(f"{study} : error")
                    print(e)
                    print(traceback.format_exc())
                    print("CRITICAL:")
            # ---
            images = [image for image in images if image]
            # ---
            if not images:
                printt(f"{study} : not found")
                images = get_images_stacks(study)
                # ---
                if not images:
                    images = get_images(f"https://radiopaedia.org/cases/{self.caseId}/studies/{study}")
                # ---
                with open(st_file, "w", encoding="utf-8") as f:
                    json.dump(images, f, ensure_ascii=False, indent=2)
            # ---
            self.studies[study] = images
            printt(f"study:{study} : len(images) = {len(images)}, st_file:{st_file}")

    def upload_images(self, study, images):
        planes = {}
        # ---
        self.img_to_url[study] = {}
        # ---
        for i, image in enumerate(images, 1):
            if not isinstance(image, dict):
                continue
            # ---
            image_url = image.get("public_filename", "")
            # ---
            if not image_url:
                continue
            # ---
            extension = image_url.split(".")[-1].lower()
            # ---
            if not extension:
                extension = image["fullscreen_filename"].split(".")[-1].lower()
            # ---
            if extension == "bmp":
                extension = "jpg"
            # ---
            image_id = image["id"]
            plane = image["plane_projection"]
            # ---
            if plane not in planes:
                planes[plane] = 0
            planes[plane] += 1
            # ---
            file_name = f"{self.title} (Radiopaedia {self.caseId}-{study} {plane} {planes[plane]}).{extension}"
            # ---
            file_name = file_name.replace("  ", " ").replace("  ", " ").replace("  ", " ")
            # ---
            file_name = file_name.replace(":", ".").replace("/", ".")
            # ---
            self.img_to_url[study][f"File:{file_name}"] = {"url": image_url, "id": image_id}

    def start(self):
        self.get_studies()

        for study, images in self.studies.items():
            printt(f"{study} : len(images) = {len(images)}")
            # ---
            self.upload_images(study, images)

        dump_studies_urls_to_files(self.img_to_url)
