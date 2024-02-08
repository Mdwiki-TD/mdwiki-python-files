'''
from mass.radio.One_Case import OneCase
'''
import sys
import os
from pathlib import Path
import pywikibot
import json
import traceback
# ---
from newapi import printe
from nccommons import api
from newapi.ncc_page import MainPage as ncc_MainPage
from mass.radio.studies import get_images_stacks, get_images
from mass.radio.bmp import work_bmp
# ---
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
main_dir = Path(__file__).parent
# --
urls_done = []


def get_image_extension(image_url):
    # Split the URL to get the filename and extension
    _, filename = os.path.split(image_url)

    # Split the filename to get the name and extension
    name, extension = os.path.splitext(filename)

    # Return the extension (without the dot)
    ext = extension[1:]
    return ext if ext else 'jpeg'


class OneCase:
    def __init__(self, case_url, caseId, title, studies_ids, author):
        self.author = author
        self.caseId = caseId
        self.case_url = case_url
        self.title = title
        self.studies_ids = studies_ids
        self.images_count = 0
        self.files = []
        self.studies = {}
        self.set_title = f'Radiopaedia case {self.caseId} {self.title}'
        self.category = f'Category:Radiopaedia case {self.caseId} {self.title}'
        # ---
        self.published = ''
        self.system = ''
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
        # ---

    def create_category(self):
        text = f'* [{self.case_url} Radiopaedia case: {self.title} ({self.caseId})]\n'
        text += f'[[Category:Radiopaedia images by case|{self.caseId}]]'
        # ---
        if self.system:
            text += f"\n[[Category:Radiopaedia cases for {self.system}]]"
        # ---
        cat = ncc_MainPage(self.category, 'www', family='nccommons')
        # ---
        if cat.exists():
            printe.output(f'<<lightyellow>> {self.category} already exists')
            return
        # ---
        new = cat.Create(text=text, summary='')
        printe.output(f'Category {self.category} created..')
        # else:
        #     if text != cat.get_text():
        #         printe.output(f'<<lightyellow>>{self.category} already exists')
        #         new = cat.save(newtext=text, summary='update', nocreate=0, minor='')
        # ---

    def get_studies(self):
        for study in self.studies_ids:
            st_file = os.path.join(str(main_dir), 'studies', f'{study}.json')
            # ---
            images = {}
            # ---
            if os.path.exists(st_file):
                try:
                    with open(st_file, 'r', encoding='utf-8') as f:
                        images = json.loads(f.read())
                except Exception as e:
                    pywikibot.output("<<lightred>> Traceback (most recent call last):")
                    printe.output(f'{study} : error')
                    pywikibot.output(e)
                    pywikibot.output(traceback.format_exc())
                    pywikibot.output("CRITICAL:")
            # ---
            images = [ image for image in images if image ]
            # ---
            if not images:
                printe.output(f'{study} : not found')
                # images = get_images(f'https://radiopaedia.org/cases/167250/studies/167250')
                # images = get_images(f'https://radiopaedia.org/cases/167250/studies/135974?lang=us')
                images = get_images_stacks(self.caseId)
                # ---
                if not images:
                    images = get_images(f'https://radiopaedia.org/cases/{self.caseId}/studies/{study}')
                # ---
                with open(st_file, 'w', encoding='utf-8') as f:
                    json.dump(images, f, ensure_ascii=False, indent=4)
            # ---
            self.studies[study] = images
            printe.output(f'study:{study} : len(images) = {len(images)}, st_file:{st_file}')

    def upload_image(self, image_url, image_name, image_id, plane, modality):
        if 'noup' in sys.argv:
            return image_name
        # ---
        file_title = f'File:{image_name}'
        # ---
        file_page = ncc_MainPage(file_title, 'www', family='nccommons')
        # ---
        if file_page.exists():
            printe.output(f'<<lightyellow>> File:{image_name} already exists')
            return image_name
        # ---
        image_text = '== {{int:summary}} ==\n'

        image_text += (
            '{{Information\n'
            f'|Description = \n'
            f'* Radiopaedia case ID: [{self.case_url} {self.caseId}]\n'
            # f'* Image ID: {image_id}\n'
            f'* Image ID: [{image_url} {image_id}]\n'
            f'* Plane projection: {plane}\n'
            f'* modality: {modality}\n'
            f'|Date = {self.published}\n'
            f'|Source = [{self.case_url} {self.title}]\n'
            f'|Author = {self.author}\n'
            '|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n'
            '}}\n'
            '== {{int:license}} ==\n'
            '{{CC-BY-NC-SA-3.0}}\n'
            f'[[{self.category}]]\n'
            '[[Category:Uploads by Mr. Ibrahem]]'
        )

        file_name = api.upload_by_url(image_name, image_text, image_url, return_file_name=True)

        printe.output(f"upload result: {file_name}")
        return file_name

    def upload_images(self, study, images):
        sets = []
        planes = {}
        modality = ''

        for image in images:
            image_url = image.get('public_filename', '')
            # ---
            if not image_url:
                print('no image')
                print(image)
                continue
            # ---
            if image_url in urls_done:
                self.images_count += 1
                continue
            # ---
            # extension = get_image_extension(image_url)
            extension = image_url.split(".")[-1].lower()
            # ---
            if extension == '':
                # extension = get_image_extension(image['fullscreen_filename'])
                extension = image['fullscreen_filename'].split(".")[-1].lower()
            # ---
            if extension != "bmp" and 'bmp' in sys.argv:
                continue
            # ---
            if extension == "bmp":
                image_url, extension = work_bmp(image_url)
            # ---
            urls_done.append(image_url)
            # ---
            image_id = image['id']
            plane = image['plane_projection']
            # ---
            if plane not in planes:
                planes[plane] = 0
            planes[plane] += 1
            # ---
            file_name = f'{self.title} (Radiopaedia {self.caseId}-{study} {plane} {planes[plane]}).{extension}'
            # ---
            file_name = file_name.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
            # ---
            # fix BadFileName
            file_name = file_name.replace(':', '.').replace('/', '.')
            # ---
            new_name = self.upload_image(image_url, file_name, image_id, plane, modality)
            # ---
            file_n = f'File:{new_name}' if new_name else f'File:{file_name}'
            # ---
            if file_n not in sets:
                self.images_count += 1
                sets.append(file_n)

        set_title = f'Radiopaedia case {self.title} id: {self.caseId} study: {study}'

        if self.images_count > 1:
            self.create_set(set_title, sets)

    def start(self):
        self.get_studies()

        for study, images in self.studies.items():
            printe.output(f'{study} : len(images) = {len(images)}')
            self.upload_images(study, images)

        printe.output(f'Images count: {self.images_count}')

        if self.images_count == 0:
            printe.output('no category created')
            return

        self.create_category()

    def create_set(self, set_title, sets):
        text = ''
        # ---
        if 'noset' in sys.argv:
            return
        # ---
        text += '{{Imagestack\n|width=850\n'
        text += f'|title={set_title}\n|align=centre\n|loop=no\n'
        # ---
        for image_name in sets:
            text += f'|{image_name}|\n'
        # ---
        text += '\n}}\n[[Category:Image set]]\n'
        text += f'[[Category:{self.set_title}|*]]\n'
        text += '[[Category:Radiopaedia sets]]'
        # ---
        page = ncc_MainPage(set_title, 'www', family='nccommons')
        # ---
        if not page.exists():
            new = page.Create(text=text, summary='')
            return new
        # ---
        # if text != page.get_text():
        #     printe.output(f'<<lightyellow>>{set_title} already exists')
        p_text = page.get_text()
        # ---
        if p_text.find('.bmp') != -1:
            p_text = p_text.replace('.bmp', '.jpg')
            ssa = page.save(newtext=p_text, summary='update', nocreate=0, minor='')
            return ssa

        elif 'fix' in sys.argv:
            if text == p_text:
                printe.output('<<lightyellow>> no changes')
                return True
            ssa = page.save(newtext=text, summary='update', nocreate=0, minor='')
            return ssa
