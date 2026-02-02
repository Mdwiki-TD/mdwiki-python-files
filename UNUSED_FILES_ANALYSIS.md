# Unused Files Analysis Report

## Overview

This document provides a comprehensive analysis of unused Python files and folders in the mdwiki-python-files repository. The analysis was performed using the `analyze_unused_files.py` script which traces all imports from defined entry points to identify code that is never used.

## Executive Summary

Based on the dependency analysis:

- **Total Python files**: 276
- **Used files**: 63 (22.8%)
- **Unused files**: 213 (77.2%)
- **Total folders with Python files**: 65
- **Completely unused folders**: 31

## Methodology

### Entry Points

The analysis starts from 23 primary entry point files that are directly executed in this repository:

1. `md_core/mdpy/find_replace_bot/bot.py`
2. `td_core/db_work/days_7.py`
3. `td_core/mdpyget/sqlviews_new.py`
4. `td_core/mdpyget/getas.py`
5. `td_core/mdpyget/enwiki_views.py`
6. `md_core/updates/io.py`
7. `md_core/updates/listo.py`
8. `md_core/updates/Medicine_articles.py`
9. `md_core/mdpy/fix_duplicate.py`
10. `md_core/add_rtt/pup.py`
11. `td_core/fix_user_pages/bot.py`
12. `md_core/fix_cs1/bot.py`
13. `md_core/fix_cs1/fix_cs_params/bot.py`
14. `td_core/mdpages/cashwd.py`
15. `td_core/copy_data/by_qid/sitelinks.py`
16. `md_core_helps/apis/cat_cach.py`
17. `td_core/copy_data/by_title/all_articles.py`
18. `td_core/copy_data/by_title/exists_db.py`
19. `td_core/wd_works/recheck.py`
20. `td_core/db_work/check_titles.py`
21. `copy_to_en/revid.py`
22. `td_core/mdcount/countref.py`
23. `td_core/mdcount/words.py`

**Note**: Two entry points were specified but not found:
- `mass/radio/cases_in_ids.py`
- `mass/radio/st3/count.py`

### Analysis Process

1. **Discover all Python files** in the repository (excluding `.git`, `__pycache__`, and `newupdater` folders)
2. **Parse each entry point file** using Python's AST module to extract all import statements
3. **Resolve imports** to actual file paths, handling:
   - Absolute imports (e.g., `from mdapi_sql import sql_for_mdwiki`)
   - Relative imports (e.g., `from . import module`)
   - Package imports (resolving to `__init__.py` files)
4. **Recursively trace dependencies** following the import chain
5. **Identify unused files** as those not in the dependency chain
6. **Identify unused folders** where all Python files are unused

## How to Run the Analysis

```bash
cd /home/runner/work/mdwiki-python-files/mdwiki-python-files
python analyze_unused_files.py
```

This will generate two reports:
- `unused_files_report.txt` - Human-readable text report
- `unused_files_report.json` - Machine-readable JSON format

## Understanding the Results

### Used Files

Files are marked as "used" if they are:
1. Entry point files themselves
2. Directly imported by any used file
3. Transitively imported through the dependency chain

Example of used files:
- `md_core/mdpy/bots/check_title.py` - Imported by `copy_to_en/revid.py`
- `mdwiki_api/mdwiki_page.py` - Imported by multiple entry points
- `md_core_helps/mdapi_sql/sql_for_mdwiki.py` - Imported by database-related scripts

### Unused Files

Files marked as "unused" are never imported by any entry point, directly or indirectly. However, before removing these files, verify:

1. **Not used by external tools** - The file may be called directly by scripts outside this repository
2. **Not dynamically imported** - Some files may be loaded at runtime using `importlib` or `__import__`
3. **Not configuration files** - Files that don't contain code but are read as data
4. **Not in documentation** - Files used as examples or referenced in docs

### Completely Unused Folders

The following folders contain ONLY unused files and could potentially be archived or removed:

- `copy_text/` (6 files)
- `copy_to_en/bots/` (6 files)
- `copy_to_en/tests/` (1 file)
- `fix_use/` (4 files)
- `md_core/add_rtt/tests/` (4 files)
- `md_core/commons_svg/` (2 files)
- `md_core/mdpy/bots/tests/` (1 file)
- `md_core/mdpy/fixref/` (4 files)
- `md_core/mdpy/others/` (5 files)
- `md_core/p11143_bot/` (4 files)
- `md_core/stats/` (7 files)
- `md_core/unlinked_wb/` (3 files)
- And 19 more folders (see full report)

## Sample Unused Files by Category

### Bot Scripts (Not in Use)
- `copy_text/bot.py`
- `fix_use/bot.py`
- `md_core/add_rtt/bot.py`
- `md_core/commons_svg/bot.py`
- `md_core/p11143_bot/bot.py`
- `md_core/unlinked_wb/bot.py`

### Helper/Utility Modules (Not in Use)
- `md_core/mdpy/bots/make_title_bot.py`
- `md_core/mdpy/fixref/fixref_text_new.py`
- `md_core_helps/apis/wiki_api.py`
- `td_core/after_translate/bots/fixcat.py`

### Test Files (Not in Use)
- `copy_to_en/tests/test_alltext_changes.py`
- `md_core/mdpy/bots/tests/test_sql_for_mdwiki.py`
- `md_core_helps/one_time/prior/tests/*.py`
- `wprefs/tests/test_es/bot.py`

### One-Time Scripts (Archived Projects)
- `md_core_helps/one_time/WHOem/` - WHO emergency project
- `md_core_helps/one_time/niosh/` - NIOSH project
- `md_core_helps/one_time/prior/` - Prior versions project
- `md_core_helps/one_time/priorviews/` - Prior views analysis
- `md_core_helps/one_time/wikiblame/` - WikiBlame integration

## Recommendations

### Immediate Actions

1. **Review the unused files list** to confirm they are truly not needed
2. **Check for dynamic imports** that the analysis might have missed
3. **Verify external dependencies** - check if any CI/CD or external scripts use these files

### Safe Cleanup Strategy

If you decide to remove unused files:

1. **Create a backup branch** before any deletions
2. **Start with obviously obsolete folders** like `one_time/` projects
3. **Remove test folders** for unused modules first
4. **Archive rather than delete** - move files to an `archived/` directory initially
5. **Monitor for issues** after each cleanup phase
6. **Update documentation** to reflect removed functionality

### Consider Keeping

Some files, even if unused in imports, might still be valuable:

- **Documentation examples** that aren't meant to be imported
- **Scripts run manually** that weren't listed as entry points
- **Configuration templates** used for setup
- **Historical reference** code that documents past approaches

## Limitations of This Analysis

This analysis may not detect:

1. **Dynamic imports** using `importlib.import_module()` or `__import__()`
2. **exec() or eval()** statements that load code at runtime
3. **External callers** from other repositories or tools
4. **Command-line scripts** not listed in the entry points
5. **Files loaded as data** rather than imported as modules

## Updating the Analysis

To update the entry points list or re-run the analysis:

1. Edit `analyze_unused_files.py` and update the `entry_points` list in `main()`
2. Run the script: `python analyze_unused_files.py`
3. Review the new reports generated

## Additional Resources

- **Full text report**: `unused_files_report.txt`
- **JSON data**: `unused_files_report.json`
- **Analysis script**: `analyze_unused_files.py`

## Contact

For questions about specific files or to report issues with the analysis:
- Review the dependency tree in `unused_files_report.txt`
- Check the `warnings` section for potential issues
- Verify imports manually for critical files

---

*Generated on: 2026-02-02*  
*Script version: 1.0*  
*Repository: Mdwiki-TD/mdwiki-python-files*
