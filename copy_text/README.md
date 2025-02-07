# README

## Overview
This repository contains a set of Python scripts designed to process and manage text and HTML content for the MedWiki project. The scripts perform various tasks such as fetching and processing wiki text, converting it to HTML, segmenting the HTML, and managing categories and pages.

## Files and Their Functions

### bot.py
This script is the main entry point for processing wiki pages. It defines a `WikiProcessor` class that handles the following tasks:
- Fetching wiki text for a given page.
- Converting the wiki text to HTML.
- Segmenting the HTML content.
- Saving the processed content to files.
- The script also includes functions to process multiple pages concurrently using multiprocessing.

```sh
python bot.py
```

### files_list.py
This script manages the list of categories and pages. It performs the following tasks:
- Fetching categories and their pages from the database.
- Sorting and organizing the categories.
- Dumping the titles of the pages into a JSON file.

### text_bot.py
This script handles the retrieval and processing of wiki text. It performs the following tasks:
- Fetching the text and revision ID of a page.
- Extracting categories from the text.
- Fixing references and making other text adjustments.
- Formatting the text for further processing.

### scan_files.py
This script scans HTML files for errors and optionally deletes files containing errors. It performs the following tasks:
- Scanning HTML files for the presence of "Wikimedia Error".
- Listing files with errors.
- Deleting files with errors if the `del` argument is provided.

#### Arguments
`scan_files.py` can be run with the `del` argument to delete files with errors:
```sh
python scan_files.py del
```

### html_bot.py
This script processes HTML content to fix specific issues. It performs the following tasks:
- Parsing HTML content using BeautifulSoup.
- Removing unwanted attributes from anchor tags.
- Fixing links by removing unnecessary query parameters.

