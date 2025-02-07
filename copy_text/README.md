# Overview
This repository contains a set of Python scripts designed to process and manage text and HTML content for the MedWiki project. The scripts perform various tasks such as fetching and processing wiki text, converting it to HTML, segmenting the HTML, and managing categories and pages.

- `files_list.py` This script manages the list of categories and pages.

# Usage
```sh
python3 core8/pwb.py copy_text/files_list
python3 core8/pwb.py copy_text/bot
```

`scan_files.py` can be run with the `del` argument to delete files with errors:

```sh
python3 core8/pwb.py copy_text/scan_files del
```

# Then
- this `Wikitext` and `Html` and `Segments` files will be used by [MdTexts Script](https://github.com/mdwikicx/medwiki.toolforge.org/tree/update/public_html/mdtexts).
