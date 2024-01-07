'''
from mass.radio.One_Case import OneCase
'''
import sys
import os
from pathlib import Path
import re
import requests
import json
#---
from nccommons import api
from new_api.ncc_page import MainPage as ncc_MainPage
from mass.radio.studies import get_images
#---
main_dir = Path(__file__).parent
#--
urls_done = []
#--
def get_image_extension(image_url):
    # Split the URL to get the filename and extension
    _, filename = os.path.split(image_url)
    
    # Split the filename to get the name and extension
    name, extension = os.path.splitext(filename)
    
    # Return the extension (without the dot)
    ext = extension[1:]
    return ext if ext else 'jpeg'

class OneCase:
    def __init__(self, case_url, caseId, title, studies_ids, pages, author):
        self.author  = author
        self.pages  = pages
        self.caseId  = caseId
        self.case_url = case_url
        self.title   = title
        self.studies_ids = studies_ids
        self.files = []
        self.studies = {}
        self.set_title = f'Radiopaedia case {self.caseId} {self.title}'
        self.category = f'Category:Radiopaedia case {self.caseId} {self.title}'
    
    def create_category(self):
        text = f'* [{self.case_url} Radiopaedia case: {self.title} ({self.caseId})]\n'
        text += f'[[Category:Radiopaedia images by case|{self.caseId}]]'
        # ---
        if self.category in self.pages:
            print(f'<<lightyellow>> {self.category} already exists')
            return
        # ---
        cat = ncc_MainPage(self.category, 'www', family='nccommons')
        # ---
        if not cat.exists():
            new = cat.Create(text=text, summary='')
            print(f'Category {self.category} created..')
        # else:
        #     if text != cat.get_text():
        #         print(f'<<lightyellow>>{self.category} already exists')
        #         new = cat.save(newtext=text, summary='update', nocreate=0, minor='')
        # ---

    def get_studies(self):

        for study in self.studies_ids:
            st_file = os.path.join(str(main_dir), 'studies', f'{study}.json')
            #---
            if os.path.exists(st_file):
                with open(st_file, 'r', encoding='utf-8') as f:
                    ja = json.loads(f.read())
                    self.studies[study] = ja
                    print(f'{study} : len(ja) = {len(ja)}')
            else:
                print(f'{study} : not found')
                images = get_images(f'https://radiopaedia.org/cases/{self.caseId}/studies/{study}')
                with open(st_file, 'w', encoding='utf-8') as f:
                    json.dump(images, f, ensure_ascii=False, indent=4)
                self.studies[study] = images
                print(f'{study} : len(images) = {len(images)}')

    def upload_image(self, image_url, image_name, image_id, plane, modality):
        if 'noup' in sys.argv:
            return image_name
        # ---
        if f'File:{image_name}' in self.pages:
            print(f'<<lightyellow>> File:{image_name} already exists')
            return image_name
        # ---
        image_text = '== {{int:summary}} ==\n'

        image_text += (
            '{{Information\n'
            f'|Description = \n'
            f'* Radiopaedia case ID: [{self.case_url} {self.caseId}]\n'
            f'* Image ID: {image_id}\n'
            f'* Plane projection: {plane}\n'
            f'* modality: {modality}\n'
            f'|Date = \n'
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

        print(f"upload result: {file_name}")
        return file_name

    def upload_images(self, study, images):
        sets = []
        planes = {}
        modality = ''

        for image in images:
            image_url = image['public_filename']
            #---
            if image_url in urls_done:
                continue
            urls_done.append(image_url)
            #---
            extension = get_image_extension(image_url)
            #---
            if extension == '':
                extension = get_image_extension(image['fullscreen_filename'])
            #---
            image_id  = image['id']
            plane  = image['plane_projection']
            #---
            if plane not in planes:
                planes[plane] = 0
            planes[plane] += 1
            #---
            file_name = f'{self.title} (Radiopaedia {self.caseId}-{study} {plane} {planes[plane]}).{extension}'
            #---
            file_name = file_name.replace('  ', ' ')
            #---
            new_name = self.upload_image(image_url, file_name, image_id, plane, modality)
            sets.append(f'File:{new_name}')

        set_title = f'Radiopaedia case {self.title} id: {self.caseId} study: {study}'
        self.create_set(set_title, sets)

    def start(self):
        self.get_studies()
        self.create_category()
        for study, images in self.studies.items():
            print(f'{study} : len(images) = {len(images)}')
            self.upload_images(study, images)

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
        if page.exists():
            if text != page.get_text():
                print(f'<<lightyellow>>{set_title} already exists')
                new = page.save(newtext=text, summary='update', nocreate=0, minor='')
                return new
        else:
            new = page.Create(text=text, summary='')
            return new
