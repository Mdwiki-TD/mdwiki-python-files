#!/usr/bin/python3
"""

python3 core8/pwb.py mdpy/find_replace_bot/bot

"""
import sys
import os

import logging
from tqdm import tqdm

from mdpy.find_replace_bot.one_job import do_one_job

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

home_dir = os.getenv("HOME")

dir2 = home_dir if home_dir else "I:/mdwiki/mdwiki"

work_dir = f"{dir2}/public_html/replace/find"


def get_jobs():
    # list of subdirs in work_dir if subdir/done.txt not exists

    dirs = os.listdir(work_dir)
    jobs = []
    done = 0
    for nn in dirs:
        if os.path.exists(f"{work_dir}/{nn}/done.txt") and "nodone" not in sys.argv:
            done += 1
            continue
        jobs.append(nn)

    print(f"done:{done}, new jobs:{len(jobs)}")

    return jobs


def main():
    try:
        jobs = get_jobs()
        logging.info(f"Found {len(jobs)} jobs to process")

        for job in tqdm(jobs, desc="Processing jobs"):
            try:
                do_one_job(job)
                logging.info(f"Successfully processed job: {job}")
            except Exception as e:
                logging.error(f"Error processing job {job}: {str(e)}")

    except Exception as e:
        logging.error(f"An error occurred in the main function: {str(e)}")

if __name__ == "__main__":
    main()
