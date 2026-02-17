# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MDWiki Python Bot is a multi-module automation tool for interacting with the MediaWiki ecosystem. It performs tasks like copying text between wiki pages, updating references, processing templates, interfacing with wiki APIs, and maintaining MDWiki content.

## Commands

### Running Tests
```bash
pytest                          # Run all tests (uses tests/ directory)
pytest tests/wprefs/bots/       # Run tests for a specific module
pytest -m "not slow"            # Run tests excluding slow ones
pytest -m unit                  # Run only unit tests
pytest -k "test_name"           # Run tests matching a name pattern
```

### Code Formatting and Linting
```bash
ruff format .                   # Format code with ruff
ruff check .                    # Lint with ruff
ruff check . --fix              # Auto-fix lint issues
mypy .                          # Type checking
pre-commit run --all-files      # Run all pre-commit hooks
```

### Running Bot Scripts
Bots are typically run via a wrapper script (`pwb.py`):
```bash
python3 core8/pwb.py copy_text/bot           # Run copy_text bot
python3 core8/pwb.py newupdater/med Aspirin  # Update specific page
python3 core8/pwb.py copy_text/scan_files del  # With arguments
```

On Toolforge:
```bash
tfj run tofiles --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py copy_text/bot"
```

## Architecture

### Core Modules

- **`mdwiki_api/`** - Low-level API wrappers for MediaWiki interaction. Contains `NEW_API` class and `MainPage` for page operations. Wraps the external `newapi` library.

- **`md_core_helps/apis/`** - High-level API helpers:
  - `mdwiki_api.py` - MDWiki-specific API operations
  - `wiki_api.py` - Wikipedia API operations
  - `wikidataapi.py` - Wikidata API operations

- **`md_core_helps/mdapi_sql/`** - Database operations for MDWiki SQL tables. Use `sql_for_mdwiki.py` for database queries.

### Bot/Task Modules

Each module contains bot scripts in `bots/` subdirectories:

- **`copy_text/`** - Copies wiki text to HTML segments for the MDWiki website
- **`copy_to_en/`** - Copies content to English Wikipedia
- **`md_core/`** - Core MDWiki operations:
  - `add_rtt/` - Add reference columns to tables
  - `fix_cs1/` - Fix Citation Style 1 templates
  - `mdpy/` - General MDWiki Python utilities
  - `stats/` - Statistics generation
- **`newupdater/`** - Updates drugbox/chembox infoboxes and moves sections
- **`td_core/`** - Translation-related tasks:
  - `after_translate/` - Post-translation processing
  - `copy_data/` - Copy data between databases
  - `mdcount/` - Count references and words
- **`wprefs/`** - Wiki preferences and text replacement utilities

### Key Utility: `replace_except`

The `wprefs/bots/replace_except.py` module provides `replaceExcept()` for regex replacement that skips protected regions (comments, templates, links, headers, etc.). Used throughout the codebase for safe text manipulation.

## Important Patterns

### External Dependency: `newapi`
The codebase relies heavily on an external `newapi` library (imported as `from newapi.super...`). This library is not defined in this repository - it's expected to be available in the Python path.

### API Usage Pattern
```python
from mdwiki_api.wiki_page import MainPage, NEW_API
# For MDWiki
from mdwiki_api.mdwiki_page import NEW_API, md_MainPage
# High-level helpers
from apis import wiki_api, mdwiki_api, wikidataapi
```

### Database Pattern
```python
from mdapi_sql import sql_for_mdwiki
# Execute queries
result = sql_for_mdwiki.mdwiki_sql(query, return_dict=True)
```

### Test Structure
Tests are consolidated in the top-level `tests/` directory. The test configuration in `pytest.ini` defines markers: `slow`, `fast`, `unit`, `skip2`, `dump`. Some tests in module subdirectories may be standalone scripts.

## Configuration

- **Python version**: 3.13 (configured in pyproject.toml)
- **Line length**: 120 characters
- **Target platforms**: Runs on Toolforge (Toolforge) and locally on Windows
- **Credentials**: Stored externally, accessed via environment or user account modules
