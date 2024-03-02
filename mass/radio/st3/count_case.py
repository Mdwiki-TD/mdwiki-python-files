'''
from mass.radio.st3.One_Case_New import OneCase
'''
import sys
import os
from pathlib import Path
import json
import traceback
# ---
from newapi import printe
from nccommons import api
from newapi.ncc_page import NEW_API, MainPage as ncc_MainPage
from mass.radio.studies import get_images_stacks, get_images
from mass.radio.bmp import work_bmp
# ---
try:
    import pywikibot
    pywikibotoutput = pywikibot.output
except ImportError:
    pywikibotoutput = print
# ---
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
api_new  = NEW_API('www', family='nccommons')
api_new.Login_to_wiki()
# ---
main_dir = Path(__file__).parent.parent
# --
urls_done = []

def printt(s):
    if 'nopr' in sys.argv:
        return
    printe.output(s)

class OneCase:
    def __init__(self, case_url, caseId, title, studies_ids):
        self.caseId = caseId
        self.case_url = case_url
        self.title = title
        self.studies_ids = studies_ids
        self.images_count = 0
        self.studies_count = len(studies_ids)


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
                    pywikibotoutput("<<lightred>> Traceback (most recent call last):")
                    printt(f'{study} : error')
                    pywikibotoutput(e)
                    pywikibotoutput(traceback.format_exc())
                    pywikibotoutput("CRITICAL:")
            # ---
            images = [ image for image in images if image ]
            # ---
            if not images:
                printt(f'{study} : not found')
                # images = get_images(f'https://radiopaedia.org/cases/167250/studies/167250')
                # images = get_images(f'https://radiopaedia.org/cases/167250/studies/135974?lang=us')
                images = get_images_stacks(self.caseId)
                # ---
                if not images:
                    images = get_images(f'https://radiopaedia.org/cases/{self.caseId}/studies/{study}')
                # ---
            self.studies[study] = images
            printt(f'study:{study} : len(images) = {len(images)}, st_file:{st_file}')

    def start(self):
        self.get_studies()

        for study, images in self.studies.items():
            printt(f'{study} : len(images) = {len(images)}')
            self.images_count += len(images)

        printt(f'Images count: {self.images_count}')

    def images(self):
        return self.images_count
    
