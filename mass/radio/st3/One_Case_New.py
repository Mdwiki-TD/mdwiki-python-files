"""
from mass.radio.st3.One_Case_New import OneCase

"""
import sys
import tqdm
import os
from pathlib import Path
import json

# ---
from nccommons import api
from newapi import printe
from newapi.ncc_page import NEW_API, MainPage as ncc_MainPage

# from mass.radio.get_studies import get_images_stacks, get_images, get_studies_from_cach
from mass.radio.get_studies import get_stacks_fixed  # (study_id, case_id, get_cach=False)
from mass.radio.bots.bmp import work_bmp
from mass.radio.bots.update import update_text_add_pd_medical, update_text
from mass.radio.bots.add_cat import add_cat_to_images  # add_cat_to_images(sets, cat_title)
from mass.radio.bots.studies_utf import dump_studies_urls_to_files
from mass.radio.jsons_files import jsons  # , dumps_jsons, ids_to_urls, urls_to_ids
from fix_mass.fix_sets.name_bots.files_names_bot import get_files_names

add_studies_cat_del_case = [
    "20060",
]
# ---
try:
    import pywikibot

    pywikibotoutput = pywikibot.output
except ImportError:
    pywikibotoutput = print
# ---

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---
main_dir = Path(__file__).parent.parent
# ---
studies_dir = Path("/data/project/mdwiki/studies")
# ---
if not os.path.exists(studies_dir):
    printe.output(f"<<red>> studies_dir {studies_dir} not found")
    studies_dir = main_dir / "studies"
    printe.output(f"<<red>> studies_dir set to {studies_dir}")
# ---
with open(os.path.join(str(main_dir), "authors_list/authors_infos.json"), encoding="utf-8") as f:
    authors_infos = json.load(f)
# ---
api_new = NEW_API("www", family="nccommons")
api_new.Login_to_wiki()
# ---
urls_done = []
# ---
PD_medical_pages = []
if "updatetext" in sys.argv:
    from mass.radio.lists.PD_medical import PD_medical_pages_def

    PD_medical_pages = PD_medical_pages_def()


def get_image_extension(image_url):
    # Split the URL to get the filename and extension
    _, filename = os.path.split(image_url)

    # Split the filename to get the name and extension
    _name, extension = os.path.splitext(filename)

    # Return the extension (without the dot)
    ext = extension[1:]
    return ext or "jpeg"


def printt(s):
    if "nopr" in sys.argv:
        return
    printe.output(s)


class OneCase:
    def __init__(self, case_url, caseId, title, studies_ids, author):
        self.author = author
        self.caseId = caseId
        self.case_url = case_url
        self.title = title
        self.studies_ids = studies_ids
        self.images_count = 0
        self.img_to_url = {}
        self.files = []
        self.urls_rep = {}
        self.studies_names_cach = {}
        self.studies = {}
        self.set_title = f"Radiopaedia case {self.caseId} {self.title}"
        self.category = f"Category:Radiopaedia case {self.caseId} {self.title}"
        # ---
        auth_location = authors_infos.get(self.author, {}).get("location", "")
        self.usa_auth = auth_location.lower().find("united states") != -1
        # ---
        self.published = ""
        self.system = ""
        # ---
        if self.case_url in jsons.infos:
            self.published = jsons.infos[self.case_url]["published"]
            # ---
            if not self.author:
                self.author = jsons.infos[self.case_url]["author"]
            # ---
            self.system = jsons.infos[self.case_url]["system"]
        else:
            if self.case_url in jsons.url_to_sys:
                self.system = jsons.url_to_sys[self.case_url]

    def get_files_names_from_urls(self, study, images):
        # ---
        maain_uurls = list({x["public_filename"] for x in images})
        # ---
        files_names = get_files_names(maain_uurls, {}, study)
        # ---
        self.studies_names_cach[study] = files_names

    def title_exists(self, title):
        # ---
        pages = api_new.Find_pages_exists_or_not([title], noprint=True)
        # ---
        if pages.get(title):
            printt(f"<<lightyellow>> api_new {title} already exists")
            return True
        # ---
        # file_page = ncc_MainPage(title, 'www', family='nccommons')
        # ---
        # if file_page.exists():
        #     printt(f'<<lightyellow>> File:{title} already exists')
        #     return True
        # ---
        return False

    def create_category(self):
        text = f"* [{self.case_url} Radiopaedia case: {self.title} ({self.caseId})]\n"
        text += f"[[Category:Radiopaedia images by case|{self.caseId}]]"
        # ---
        if self.system:
            text += f"\n[[Category:Radiopaedia cases for {self.system}]]"
        # ---
        if self.title_exists(self.category):
            return
        # ---
        cat = ncc_MainPage(self.category, "www", family="nccommons")
        # ---
        if cat.exists():
            printt(f"<<lightyellow>> {self.category} already exists")
            return
        # ---
        new = cat.Create(text=text, summary="create")

        printt(f"Category {self.category} created..{new=}")

    def get_studies_d(self):
        for study in self.studies_ids:
            # ---
            images = get_stacks_fixed(study, self.caseId, get_cach=True)
            # ---
            # sort images by position key
            # images = sorted(images, key=lambda x: x["position"])
            # ---
            self.get_files_names_from_urls(study, images)
            # ---
            print(f"len of self.studies_names_cach[{study}] : {len(self.studies_names_cach.get(study))}")
            # ---
            self.studies[study] = images
            printt(f"study:{study} : len(images) = {len(images)}..")

    def make_image_text(self, image_url, image_id, plane, modality, study_id):
        auth_line = f"{self.author}"
        # ---
        auth_url = authors_infos.get(self.author, {}).get("url", "")
        auth_location = authors_infos.get(self.author, {}).get("location", "")
        if auth_url:
            auth_line = f"[{auth_url} {self.author}]"
        # ---
        image_url = self.urls_rep.get(image_url, image_url)
        # ---
        usa_license = ""
        # ---
        if self.usa_auth:
            usa_license = "{{PD-medical}}"
        # ---
        study_url = f"https://radiopaedia.org/cases/{self.caseId}/studies/{study_id}"
        # ---
        set_cat = ""
        # ---
        if len(self.studies) > 1 or str(study_id) in add_studies_cat_del_case or "del2" in sys.argv:
            set_cat = f"[[Category:Radiopaedia case {self.title} id: {self.caseId} study: {study_id}]]"
        # ---
        cat_case = f"[[{self.category}]]"
        # ---
        if (str(study_id) in add_studies_cat_del_case or "del2" in sys.argv) and set_cat:
            cat_case = ""
        # ---
        image_text = "== {{int:summary}} ==\n"

        image_text += (
            "{{Information\n"
            f"|Description = \n"
            f"* Radiopaedia case ID: [{self.case_url} {self.caseId}]\n"
            f"* Study ID: [{study_url} {study_id}]\n"
            f"* Image ID: [{image_url} {image_id}]\n"
            f"* Plane projection: {plane}\n"
            f"* Modality: {modality}\n"
            f"* System: {self.system}\n"
            f"* Author location: {auth_location}\n"
            f"|Date = {self.published}\n"
            f"|Source = [{self.case_url} {self.title}]\n"
            f"|Author = {auth_line}\n"
            "|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n"
            "}}\n"
            "== {{int:license}} ==\n"
            "{{CC-BY-NC-SA-3.0}}\n"
            f"{usa_license}\n"
            f"{cat_case}\n"
            "[[Category:Uploads by Mr. Ibrahem]]\n"
            f"{set_cat}"
        )
        return image_text

    def upload_image(self, image_url, image_name, image_id, plane, modality, study_id):
        if "noup" in sys.argv:
            return image_name
        # ---
        file_title = f"File:{image_name}"
        # ---
        exists = self.title_exists(file_title)
        # ---
        if exists:
            return image_name
        # ---
        image_url = self.urls_rep.get(image_url, image_url)
        # ---
        image_text = self.make_image_text(image_url, image_id, plane, modality, study_id)

        file_name = api.upload_by_url(image_name, image_text, image_url, return_file_name=True, do_ext=True)

        printt(f"upload result: {file_name}")
        if file_name and file_name != image_name:
            # ---
            if self.usa_auth and "updatetext" in sys.argv and f"File:{file_name}" not in PD_medical_pages:
                update_text_add_pd_medical(f"File:{file_name}")
            # ---
            self.add_category(file_name)

        return file_name

    def update_images_text(self, to_up, already_in):
        # ---
        tits1 = [x for x in already_in if x in to_up]
        # ---
        if self.usa_auth:
            tits2 = [x for x in tits1 if f"File:{x}" not in PD_medical_pages]
            printt(f"{len(tits1)=}, not in PD_medical_pages: {len(tits2)=}")
        else:
            tits2 = tits1
            printt(f"{len(tits1)=}, {len(tits2)=}")
        # ---
        for fa in tqdm.tqdm(tits2):
            image_url, file_name, image_id, plane, modality, study_id = to_up[fa]
            # ---
            image_url = self.urls_rep.get(image_url, image_url)
            # ---
            image_text = self.make_image_text(image_url, image_id, plane, modality, study_id)
            # ---
            file_title = f"File:{file_name}"
            # ---
            if self.usa_auth:
                update_text_add_pd_medical(file_title)
            else:
                update_text(file_title, image_text)

    def study_set_works(self, to_up, pages, study, already_in):
        # ---
        set_files = []
        # ---
        for fa in already_in:
            if fa not in set_files:
                self.images_count += 1
                set_files.append(fa)
        # ---
        not_in = {k: v for k, v in to_up.items() if not pages.get(k)}
        # ---
        printt(f"not_in: {len(not_in)}")
        # ---
        for i, (image_url, file_name, image_id, plane, modality, study_o) in enumerate(not_in.values(), 1):
            # ---
            printt(f"file: {i}/{len(not_in)} :{file_name}")
            # ---
            new_name = self.upload_image(image_url, file_name, image_id, plane, modality, study_o)
            # ---
            file_n = f"File:{new_name}" if new_name else f"File:{file_name}"
            # ---
            if file_n not in set_files:
                self.images_count += 1
                set_files.append(file_n)
        # ---
        set_title = f"Radiopaedia case {self.title} id: {self.caseId} study: {study}"
        # ---
        if ("updatetext" not in sys.argv or "del2" in sys.argv) and self.images_count > 1:
            self.create_set(set_title, set_files)
            self.create_set_category(set_title, set_files, study)

    def upload_images(self, study, images):
        planes = {}
        modality = ""
        # ---
        to_up = {}
        # ---
        self.img_to_url[study] = {}
        # ---
        for _i, image in enumerate(images, 1):
            public_filename = image.get("public_filename", "")
            image_url = image.get("public_filename", "")
            # ---
            if not image_url:
                printt("no image")
                printt(image)
                continue
            # ---
            if image_url in urls_done:
                self.images_count += 1
                continue
            # ---
            # extension = get_image_extension(image_url)
            extension = image_url.split(".")[-1].lower()
            # ---
            if not extension:
                extension = image["fullscreen_filename"].split(".")[-1].lower()
            # ---
            if extension == "bmp":
                if "dump_studies_urls_to_files" not in sys.argv:
                    image_url2, extension = work_bmp(image_url)
                    self.urls_rep[image_url2] = image_url
                    image_url = image_url2
                else:
                    extension = "jpg"
            # ---
            urls_done.append(image_url)
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
            # fix BadFileName
            file_name = file_name.replace(":", ".").replace("/", ".")
            # ---
            na_in_cach = self.studies_names_cach[study].get(public_filename)
            # print(f"{na_in_cach=}")
            # ---
            if na_in_cach and "noc" not in sys.argv:
                file_name = na_in_cach.replace("File:", "")
                printe.output(f"<<yellow>> make File name from studies_names_cach: {file_name}")
            # ---
            to_up[f"File:{file_name}"] = (image_url, file_name, image_id, plane, modality, study)
            # ---
            self.img_to_url[study][f"File:{file_name}"] = {"url": image_url, "id": image_id}
        # ---
        if "dump_studies_urls_to_files" in sys.argv:
            return
        # ---
        to_c = list(to_up.keys())
        # ---
        pages = api_new.Find_pages_exists_or_not(to_c)
        # ---
        # print(pages)
        # ---
        already_in = [k for k in to_up if pages.get(k)]
        # ---
        printt(f"already_in: {len(already_in)}")
        # ---
        if "updatetext" in sys.argv:
            # ---
            self.update_images_text(to_up, already_in)
        # ---
        self.study_set_works(to_up, pages, study, already_in)
        # ---

    def start(self):
        self.get_studies_d()

        for study, images in self.studies.items():
            printt(f"{study} : len(images) = {len(images)}")
            # ---
            self.upload_images(study, images)

        if self.img_to_url:
            dump_studies_urls_to_files(self.img_to_url)

        if "dump_studies_urls_to_files" in sys.argv:
            return

        printt(f"Images count: {self.images_count}")

        if self.images_count == 0:
            printt("no category created")
            return

        self.create_category()

    def create_set(self, set_title, set_files):
        text = ""
        # ---
        if "noset" in sys.argv:
            return
        # ---
        set_files = [x.strip() for x in set_files if x.strip()]
        # ---
        if len(set_files) < 2:
            return
        # ---
        if self.title_exists(set_title):
            return
        # ---
        text += "{{Imagestack\n|width=850\n"
        text += f"|title={set_title}\n|align=centre\n|loop=no\n"
        # ---
        for image_name in set_files:
            text += f"|{image_name}|\n"
        # ---
        text += "\n}}\n[[Category:Image set]]\n"
        text += f"[[Category:{self.set_title}|*]]\n"
        text += "[[Category:Radiopaedia sets]]"
        # ---
        page = ncc_MainPage(set_title, "www", family="nccommons")
        # ---
        if not page.exists():
            new = page.Create(text=text, summary="")
            return new
        # ---
        # if text != page.get_text():
        #     printt(f'<<lightyellow>>{set_title} already exists')
        p_text = page.get_text()
        # ---
        if p_text.find(".bmp") != -1:
            p_text = p_text.replace(".bmp", ".jpg")
            ssa = page.save(newtext=p_text, summary="update", nocreate=0, minor="")
            return ssa

        elif "fix" in sys.argv:
            if text == p_text:
                printt("<<lightyellow>> no changes")
                return True
            ssa = page.save(newtext=text, summary="update", nocreate=0, minor="")
            return ssa

    def create_set_category(self, set_title, set_files, study_id):
        # ---
        if "create_set_category" in sys.argv:
            return
        # ---
        study_url = f"https://radiopaedia.org/cases/{self.caseId}/studies/{study_id}"
        # ---
        cat_title = f"Category:{set_title}"
        # ---
        printe.output(f"len of set_files: {len(set_files)} /// cat_title:{cat_title}")
        # ---
        if len(self.studies) == 1 and "c_it" not in sys.argv:
            printe.output(f"len of self.studies: {len(self.studies)}, return (don't create set cats for 1 study)")
            printe.output("add 'c_it' to sys.argv to create set cats for 1 study")
            return
        # ---
        text = f"* [{study_url} study: {study_id}]"
        text += f"\n[[{self.category}|*]]"
        text += f"\n[[Category:Radiopaedia studies|{study_id}]]"
        # ---
        done = False
        # ---
        if self.title_exists(cat_title):
            done = True
        # ---
        if not done:
            cat = ncc_MainPage(cat_title, "www", family="nccommons")
            # ---
            if cat.exists():
                printt(f"<<lightyellow>> {cat_title} already exists")
                done = True
        # ---
        if not done:
            new = cat.Create(text=text, summary="create")
            # ---
            if new:
                done = True
            # ---
            printt(f"Category {cat_title} created..{new=}")
        # ---
        if done:
            add_cat_to_images(set_files, cat_title, self.category)

    def add_category(self, file_name):
        # ---
        if "add_category" not in sys.argv:
            return
        # ---
        add_text = f"\n[[{self.category}]]"
        # ---
        file_title = f"File:{file_name}"
        # ---
        page = ncc_MainPage(file_title, "www", family="nccommons")
        # ---
        p_text = page.get_text()
        # ---
        if p_text.find("[[Category:Radiopaedia case") != -1:
            printe.output(f"<<lightyellow>>{file_title} has cat:")
            printe.output(p_text)
        # ---
        if p_text.find(self.category) == -1:
            new_text = p_text + add_text
            ssa = page.save(newtext=new_text, summary=f"Bot: added [[:{self.category}]]")
            return ssa
