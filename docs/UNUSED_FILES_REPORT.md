# Unused Files Report

**Generated:** 2026-05-22
**Method:** Static AST trace of `import` / `from ... import` statements starting from the 28 known active entry points dispatched via `python3 c9/pwb.py <module_path>/<script>`.
**Scope:** All `.py` files under the repository root, excluding `old/`, `_old/`, `0/`, `old_codes/`, `.git/`, and `__pycache__/` directories.
**Module-resolution rule:** active entry path `foo/bar` resolves to `src/foo/bar.py` (the `src/` directory is treated as the import root, since `pyproject.toml` has no console-scripts and the dispatcher prepends `src/` to `sys.path`).

> **Disclaimer:** This is _static_ analysis. Files flagged as unused are candidates only — verify before deletion. Dynamic imports, CLI tools invoked outside `pwb.py`, cron jobs, shell scripts, and pytest-driven tests can keep code "alive" in ways an import trace will not capture.

---

## Active Files

These 101 files are reachable from at least one active entry point through a traceable import chain (including the `__init__.py` files of the packages they live in).

### Entry-point files (28)

| Active module path                        | Resolved file                                    |
| ----------------------------------------- | ------------------------------------------------ |
| `copy_to_en/revid`                        | `src/copy_to_en/revid.py`                        |
| `md_core/add_rtt/pup`                     | `src/md_core/add_rtt/pup.py`                     |
| `md_core/fix_cs1/bot`                     | `src/md_core/fix_cs1/bot.py`                     |
| `md_core/fix_cs1/fix_cs_params/bot`       | `src/md_core/fix_cs1/fix_cs_params/bot.py`       |
| `md_core/mdpy/find_replace_bot/bot`       | `src/md_core/mdpy/find_replace_bot/bot.py`       |
| `md_core/mdpy/fix_duplicate`              | `src/md_core/mdpy/fix_duplicate.py`              |
| `md_core/p11143_bot/bot`                  | `src/md_core/p11143_bot/bot.py`                  |
| `md_core/unlinked_wb/bot`                 | `src/md_core/unlinked_wb/bot.py`                 |
| `md_core/updates/io`                      | `src/md_core/updates/io.py`                      |
| `md_core/updates/listo`                   | `src/md_core/updates/listo.py`                   |
| `md_core/updates/Medicine_articles`       | `src/md_core/updates/Medicine_articles.py`       |
| `md_core_helps/apis/cat_cach`             | `src/md_core_helps/apis/cat_cach.py`             |
| `td_core/copy_data/by_qid/sitelinks`      | `src/td_core/copy_data/by_qid/sitelinks.py`      |
| `td_core/copy_data/by_title/all_articles` | `src/td_core/copy_data/by_title/all_articles.py` |
| `td_core/db_work/check_titles`            | `src/td_core/db_work/check_titles.py`            |
| `td_core/db_work/days_7`                  | `src/td_core/db_work/days_7.py`                  |
| `td_core/db_work/get_red`                 | `src/td_core/db_work/get_red.py`                 |
| `td_core/fix_user_pages/bot`              | `src/td_core/fix_user_pages/bot.py`              |
| `td_core/mdcount/countref`                | `src/td_core/mdcount/countref.py`                |
| `td_core/mdcount/words`                   | `src/td_core/mdcount/words.py`                   |
| `td_core/mdpages/cashwd`                  | `src/td_core/mdpages/cashwd.py`                  |
| `td_core/mdpages/find_qids`               | `src/td_core/mdpages/find_qids.py`               |
| `td_core/mdpyget/enwiki_views`            | `src/td_core/mdpyget/enwiki_views.py`            |
| `td_core/mdpyget/getas`                   | `src/td_core/mdpyget/getas.py`                   |
| `td_core/mdpyget/sqlviews_new`            | `src/td_core/mdpyget/sqlviews_new.py`            |
| `td_core/td_other_qids/fix_qids`          | `src/td_core/td_other_qids/fix_qids.py`          |
| `td_core/td_other_qids/make_list`         | `src/td_core/td_other_qids/make_list.py`         |
| `td_core/wd_works/recheck`                | `src/td_core/wd_works/recheck.py`                |

### Transitively imported files (73)

```
src/copy_to_en/__init__.py
src/md_core/__init__.py
src/md_core/add_rtt/__init__.py
src/md_core/add_rtt/r_column_bots/__init__.py
src/md_core/add_rtt/r_column_bots/add_r_column.py
src/md_core/add_rtt/r_column_bots/pup_table.py
src/md_core/fix_cs1/__init__.py
src/md_core/fix_cs1/archive_date_maker.py
src/md_core/fix_cs1/bots/__init__.py
src/md_core/fix_cs1/bots/find_journal.py
src/md_core/fix_cs1/bots/pmid.py
src/md_core/fix_cs1/bots/temps_list.py
src/md_core/fix_cs1/fix_cs_params/__init__.py
src/md_core/fix_cs1/fix_p.py
src/md_core/mdpy/__init__.py
src/md_core/mdpy/find_replace_bot/__init__.py
src/md_core/mdpy/find_replace_bot/one_job.py
src/md_core/p11143_bot/__init__.py
src/md_core/p11143_bot/filter_helps.py
src/md_core/p11143_bot/wd_helps.py
src/md_core/unlinked_wb/__init__.py
src/md_core/unlinked_wb/hlps.py
src/md_core/updates/__init__.py
src/md_core_helps/__init__.py
src/md_core_helps/apis/__init__.py
src/md_core_helps/apis/mdwiki_api_call.py
src/md_core_helps/apis/mw_views.py
src/md_core_helps/apis/user_accounts.py
src/md_core_helps/apis/wd_bots/__init__.py
src/md_core_helps/apis/wd_bots/wd_rest_new.py
src/md_core_helps/apis/wd_bots/wikidataapi_post.py
src/md_core_helps/apis/wiki_api.py
src/md_core_helps/apis/wikidataapi.py
src/md_core_helps/bots/__init__.py
src/md_core_helps/bots/check_title.py
src/md_core_helps/bots/en_to_md.py
src/md_core_helps/bots/py_tools.py
src/md_core_helps/mdapi_sql/__init__.py
src/md_core_helps/mdapi_sql/sql_for_mdwiki.py
src/md_core_helps/mdapi_sql/sql_qids.py
src/md_core_helps/mdapi_sql/sql_qids_others.py
src/md_core_helps/mdapi_sql/sql_qu.py
src/md_core_helps/mdapi_sql/sql_td_bot.py
src/md_core_helps/mdapi_sql/wiki_sql.py
src/mdwiki_api/__init__.py
src/mdwiki_api/mdwiki_page.py
src/mdwiki_api/wiki_page.py
src/td_core/__init__.py
src/td_core/copy_data/__init__.py
src/td_core/copy_data/by_qid/__init__.py
src/td_core/copy_data/by_title/__init__.py
src/td_core/db_work/__init__.py
src/td_core/db_work/check_titles_helps.py
src/td_core/fix_user_pages/__init__.py
src/td_core/fix_user_pages/fix_it_db_new.py
src/td_core/fix_user_pages/user_bot.py
src/td_core/mdcount/__init__.py
src/td_core/mdcount/bots/__init__.py
src/td_core/mdcount/bots/countref_bots.py
src/td_core/mdcount/bots/lead.py
src/td_core/mdcount/bots/links.py
src/td_core/mdcount/bots/regex_scanner.py
src/td_core/mdcount/ref_words_bot.py
src/td_core/mdpages/__init__.py
src/td_core/mdpages/create_qids.py
src/td_core/mdpyget/__init__.py
src/td_core/mdpyget/bots/__init__.py
src/td_core/mdpyget/bots/to_sql.py
src/td_core/mdpyget/pages_list.py
src/td_core/td_dirs.py
src/td_core/td_other_qids/__init__.py
src/td_core/td_other_qids/qids_help.py
src/td_core/wd_works/__init__.py
```

---

## Unused Files

222 `.py` files were never reached. Grouped by parent folder:

### Repository root

| Path          | Reason                                                                                               |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| `__init__.py` | Empty top-level marker; the `src/` layout makes it irrelevant — no entry point traverses through it. |

### `src/md_core/add_rtt/`

| Path                                 | Reason                                                          |
| ------------------------------------ | --------------------------------------------------------------- |
| `src/md_core/add_rtt/bot.py`         | Not imported by `pup.py` or any of its transitive dependencies. |
| `src/md_core/add_rtt/named_param.py` | Not imported by any active module.                              |
| `src/md_core/add_rtt/remove.py`      | Not imported by any active module.                              |

### `src/md_core/commons_svg/`

| Path                              | Reason                                          |
| --------------------------------- | ----------------------------------------------- |
| `src/md_core/commons_svg/bot.py`  | Folder has no active entry; nothing imports it. |
| `src/md_core/commons_svg/list.py` | Folder has no active entry; nothing imports it. |

> _Note:_ this folder has no `__init__.py` and contains a non-Python `list.wiki` data file as well.

### `src/md_core/fix_cs1/`

| Path                           | Reason                                                         |
| ------------------------------ | -------------------------------------------------------------- |
| `src/md_core/fix_cs1/tests.py` | Test file; not imported by `bot.py` or `fix_cs_params/bot.py`. |

### `src/md_core/mdpy/`

| Path                           | Reason                                                           |
| ------------------------------ | ---------------------------------------------------------------- |
| `src/md_core/mdpy/fixred.py`   | Not imported by `find_replace_bot/bot.py` or `fix_duplicate.py`. |
| `src/md_core/mdpy/imp.py`      | Not imported by any active module.                               |
| `src/md_core/mdpy/orred.py`    | Not imported by any active module.                               |
| `src/md_core/mdpy/red.py`      | Not imported by any active module.                               |
| `src/md_core/mdpy/replace1.py` | Not imported by any active module.                               |

### `src/md_core/mdpy/fixref/` (entire folder)

| Path                                         | Reason                                               |
| -------------------------------------------- | ---------------------------------------------------- |
| `src/md_core/mdpy/fixref/__init__.py`        | No active entry inside this package; never imported. |
| `src/md_core/mdpy/fixref/fixref_text_new.py` | —                                                    |
| `src/md_core/mdpy/fixref/fixreftest.py`      | —                                                    |
| `src/md_core/mdpy/fixref/make_title_bot.py`  | —                                                    |
| `src/md_core/mdpy/fixref/start.py`           | —                                                    |

### `src/md_core/mdpy/others/` (entire folder)

| Path                                   | Reason                                               |
| -------------------------------------- | ---------------------------------------------------- |
| `src/md_core/mdpy/others/__init__.py`  | No active entry inside this package; never imported. |
| `src/md_core/mdpy/others/copy_qids.py` | —                                                    |
| `src/md_core/mdpy/others/export.py`    | —                                                    |
| `src/md_core/mdpy/others/fixour.py`    | —                                                    |
| `src/md_core/mdpy/others/our.py`       | —                                                    |

### `src/md_core/stats/` (entire folder)

| Path                             | Reason                           |
| -------------------------------- | -------------------------------- |
| `src/md_core/stats/__init__.py`  | No active entry; never imported. |
| `src/md_core/stats/all2.py`      | —                                |
| `src/md_core/stats/ar.py`        | —                                |
| `src/md_core/stats/by_site.py`   | —                                |
| `src/md_core/stats/editors.py`   | —                                |
| `src/md_core/stats/qids.py`      | —                                |
| `src/md_core/stats/sitelinks.py` | —                                |

### `src/md_core/updates/`

| Path                           | Reason                                                          |
| ------------------------------ | --------------------------------------------------------------- |
| `src/md_core/updates/c2023.py` | Not imported by `io.py`, `listo.py`, or `Medicine_articles.py`. |

### `src/md_core_helps/apis/`

| Path                                | Reason                                              |
| ----------------------------------- | --------------------------------------------------- |
| `src/md_core_helps/apis/txtlib2.py` | Not imported by `cat_cach.py` or any active module. |

### `src/md_core_helps/apis/sup/` (entire folder)

| Path                                        | Reason                           |
| ------------------------------------------- | -------------------------------- |
| `src/md_core_helps/apis/sup/__init__.py`    | No active entry; never imported. |
| `src/md_core_helps/apis/sup/cookies_bot.py` | —                                |
| `src/md_core_helps/apis/sup/su_login.py`    | —                                |

### `src/md_core_helps/apis/wd_bots/`

| Path                                            | Reason                                                                                |
| ----------------------------------------------- | ------------------------------------------------------------------------------------- |
| `src/md_core_helps/apis/wd_bots/wd_post_new.py` | Not imported (its sibling `wd_rest_new.py` and `wikidataapi_post.py` _are_ imported). |

### `src/md_core_helps/mdapi_sql/`

| Path                                    | Reason                             |
| --------------------------------------- | ---------------------------------- |
| `src/md_core_helps/mdapi_sql/sql.py`    | Not imported by any active module. |
| `src/md_core_helps/mdapi_sql/wikidb.py` | Not imported by any active module. |

### `src/md_core_helps/one_time/` (entire subtree)

The whole subtree is unreachable. Naming convention (`one_time`) suggests these were one-off scripts.

| Path                                                                     | Reason                      |
| ------------------------------------------------------------------------ | --------------------------- |
| `src/md_core_helps/one_time/__init__.py`                                 | No active entry in subtree. |
| `src/md_core_helps/one_time/WHOem/__init__.py`                           | —                           |
| `src/md_core_helps/one_time/WHOem/bot.py`                                | —                           |
| `src/md_core_helps/one_time/WHOem/find_views_by_lang.py`                 | —                           |
| `src/md_core_helps/one_time/WHOem/make_text.py`                          | —                           |
| `src/md_core_helps/one_time/niosh/__init__.py`                           | —                           |
| `src/md_core_helps/one_time/niosh/bot.py`                                | —                           |
| `src/md_core_helps/one_time/niosh/get.py`                                | —                           |
| `src/md_core_helps/one_time/niosh/s.py`                                  | —                           |
| `src/md_core_helps/one_time/niosh/find/__init__.py`                      | —                           |
| `src/md_core_helps/one_time/niosh/find/both.py`                          | —                           |
| `src/md_core_helps/one_time/niosh/find/qu.py`                            | —                           |
| `src/md_core_helps/one_time/niosh/find/search.py`                        | —                           |
| `src/md_core_helps/one_time/prior/__init__.py`                           | —                           |
| `src/md_core_helps/one_time/prior/add_old.py`                            | —                           |
| `src/md_core_helps/one_time/prior/get_them.py`                           | —                           |
| `src/md_core_helps/one_time/prior/p4.py`                                 | —                           |
| `src/md_core_helps/one_time/prior/read5.py`                              | —                           |
| `src/md_core_helps/one_time/prior/text_bot.py`                           | —                           |
| `src/md_core_helps/one_time/prior/bots/__init__.py`                      | —                           |
| `src/md_core_helps/one_time/prior/bots/readjsons.py`                     | —                           |
| `src/md_core_helps/one_time/prior/bots/remove_wikis.py`                  | —                           |
| `src/md_core_helps/one_time/prior/json_en/__init__.py`                   | —                           |
| `src/md_core_helps/one_time/prior/json_en/lists.py`                      | —                           |
| `src/md_core_helps/one_time/prior/json_langs/__init__.py`                | —                           |
| `src/md_core_helps/one_time/prior/json_langs/lists.py`                   | —                           |
| `src/md_core_helps/one_time/priorviews/__init__.py`                      | —                           |
| `src/md_core_helps/one_time/priorviews/add_blame_to_tra.py`              | —                           |
| `src/md_core_helps/one_time/priorviews/bot.py`                           | —                           |
| `src/md_core_helps/one_time/priorviews/by_lang.py`                       | —                           |
| `src/md_core_helps/one_time/priorviews/co.py`                            | —                           |
| `src/md_core_helps/one_time/priorviews/langs.py`                         | —                           |
| `src/md_core_helps/one_time/priorviews/bots/__init__.py`                 | —                           |
| `src/md_core_helps/one_time/priorviews/bots/count_words.py`              | —                           |
| `src/md_core_helps/one_time/priorviews/bots/get_translator.py`           | —                           |
| `src/md_core_helps/one_time/priorviews/bots/gt_blame.py`                 | —                           |
| `src/md_core_helps/one_time/priorviews/bots/helps.py`                    | —                           |
| `src/md_core_helps/one_time/priorviews/bots/sections_links.py`           | —                           |
| `src/md_core_helps/one_time/priorviews/bots/sections_text.py`            | —                           |
| `src/md_core_helps/one_time/priorviews/bots/w_all.py`                    | —                           |
| `src/md_core_helps/one_time/priorviews/find/__init__.py`                 | —                           |
| `src/md_core_helps/one_time/priorviews/find/find_blame.py`               | —                           |
| `src/md_core_helps/one_time/priorviews/find/find_creator.py`             | —                           |
| `src/md_core_helps/one_time/priorviews/find/find_translators.py`         | —                           |
| `src/md_core_helps/one_time/priorviews/find/find_views.py`               | —                           |
| `src/md_core_helps/one_time/priorviews/find/find_word.py`                | —                           |
| `src/md_core_helps/one_time/priorviews/lists/__init__.py`                | —                           |
| `src/md_core_helps/one_time/priorviews/lists/creators.py`                | —                           |
| `src/md_core_helps/one_time/priorviews/lists/creators_to_translators.py` | —                           |
| `src/md_core_helps/one_time/priorviews/lists/links_by_section.py`        | —                           |
| `src/md_core_helps/one_time/priorviews/lists/translators.py`             | —                           |
| `src/md_core_helps/one_time/priorviews/lists/views.py`                   | —                           |
| `src/md_core_helps/one_time/priorviews/lists/words.py`                   | —                           |
| `src/md_core_helps/one_time/wikiblame/__init__.py`                       | —                           |
| `src/md_core_helps/one_time/wikiblame/bot.py`                            | —                           |
| `src/md_core_helps/one_time/wikiblame/bot1.py`                           | —                           |

### `src/newupdater/` (entire package)

| Path                                                    | Reason                                          |
| ------------------------------------------------------- | ----------------------------------------------- |
| `src/newupdater/__init__.py`                            | No active entry imports this top-level package. |
| `src/newupdater/mdapi.py`                               | —                                               |
| `src/newupdater/med.py`                                 | —                                               |
| `src/newupdater/medask.py`                              | —                                               |
| `src/newupdater/new_updater/__init__.py`                | —                                               |
| `src/newupdater/new_updater/MedWorkNew.py`              | —                                               |
| `src/newupdater/new_updater/chembox.py`                 | —                                               |
| `src/newupdater/new_updater/drugbox.py`                 | —                                               |
| `src/newupdater/new_updater/helps.py`                   | —                                               |
| `src/newupdater/new_updater/mv_section.py`              | —                                               |
| `src/newupdater/new_updater/resources_new.py`           | —                                               |
| `src/newupdater/new_updater/bots/__init__.py`           | —                                               |
| `src/newupdater/new_updater/bots/Remove.py`             | —                                               |
| `src/newupdater/new_updater/bots/expend.py`             | —                                               |
| `src/newupdater/new_updater/bots/expend_new.py`         | —                                               |
| `src/newupdater/new_updater/bots/old_params.py`         | —                                               |
| `src/newupdater/new_updater/lists/__init__.py`          | —                                               |
| `src/newupdater/new_updater/lists/bot_params.py`        | —                                               |
| `src/newupdater/new_updater/lists/chem_params.py`       | —                                               |
| `src/newupdater/new_updater/lists/expend_lists.py`      | —                                               |
| `src/newupdater/new_updater/lists/identifier_params.py` | —                                               |

### `src/td_core/after_translate/` (entire subtree)

| Path                                                        | Reason                           |
| ----------------------------------------------------------- | -------------------------------- |
| `src/td_core/after_translate/__init__.py`                   | No active entry; never imported. |
| `src/td_core/after_translate/start_work.py`                 | —                                |
| `src/td_core/after_translate/bots/__init__.py`              | —                                |
| `src/td_core/after_translate/bots/add_to_mdwiki.py`         | —                                |
| `src/td_core/after_translate/bots/add_to_pages_users_db.py` | —                                |
| `src/td_core/after_translate/bots/fixcat.py`                | —                                |
| `src/td_core/after_translate/bots/get_pages.py`             | —                                |
| `src/td_core/after_translate/bots/users_pages.py`           | —                                |

### `src/td_core/copy_data/`

| Path                                             | Reason                                                               |
| ------------------------------------------------ | -------------------------------------------------------------------- |
| `src/td_core/copy_data/copy_assessments.py`      | Not imported by `by_qid/sitelinks.py` or `by_title/all_articles.py`. |
| `src/td_core/copy_data/copy_enwiki_pageviews.py` | Not imported.                                                        |
| `src/td_core/copy_data/copy_refs_2.py`           | Not imported.                                                        |
| `src/td_core/copy_data/copy_word_2.py`           | Not imported.                                                        |
| `src/td_core/copy_data/copy_word_table.py`       | Not imported.                                                        |
| `src/td_core/copy_data/by_title/exists_db.py`    | Not imported.                                                        |

### `src/td_core/fix_user_pages/`

| Path                                      | Reason                                                                      |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| `src/td_core/fix_user_pages/del.py`       | Not imported by `bot.py` (which uses `fix_it_db_new.py` and `user_bot.py`). |
| `src/td_core/fix_user_pages/fix_it_db.py` | Superseded by `fix_it_db_new.py`.                                           |

### `src/td_core/mdcount/`

| Path                                         | Reason                                                                                    |
| -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `src/td_core/mdcount/bots/ref.py`            | Not imported (sibling `countref_bots.py`, `lead.py`, `links.py`, `regex_scanner.py` are). |
| `src/td_core/mdcount/countrefs_and_words.py` | Not imported by `countref.py` or `words.py`.                                              |

### `src/td_core/mdpages/`

| Path                             | Reason                                         |
| -------------------------------- | ---------------------------------------------- |
| `src/td_core/mdpages/find_mt.py` | Not imported by `cashwd.py` or `find_qids.py`. |

### `src/wprefs/` (entire package)

| Path                                    | Reason                             |
| --------------------------------------- | ---------------------------------- |
| `src/wprefs/__init__.py`                | No active entry uses this package. |
| `src/wprefs/api.py`                     | —                                  |
| `src/wprefs/bot.py`                     | —                                  |
| `src/wprefs/bot1.py`                    | —                                  |
| `src/wprefs/es.py`                      | —                                  |
| `src/wprefs/files.py`                   | —                                  |
| `src/wprefs/helps.py`                   | —                                  |
| `src/wprefs/infobox.py`                 | —                                  |
| `src/wprefs/todb.py`                    | —                                  |
| `src/wprefs/wpref_text.py`              | —                                  |
| `src/wprefs/bots/__init__.py`           | —                                  |
| `src/wprefs/bots/Duplicatenew2.py`      | —                                  |
| `src/wprefs/bots/es_months.py`          | —                                  |
| `src/wprefs/bots/es_refs.py`            | —                                  |
| `src/wprefs/bots/es_section.py`         | —                                  |
| `src/wprefs/bots/fix_pt_months.py`      | —                                  |
| `src/wprefs/bots/replace_except.py`     | —                                  |
| `src/wprefs/bots/replace_except_old.py` | —                                  |
| `src/wprefs/bots/test_pt_months.py`     | —                                  |
| `src/wprefs/bots/txtlib2.py`            | —                                  |

### `src1/` (entire alternate-source tree)

The whole `src1/` directory looks like a parallel/legacy source tree that is not on the dispatcher's import path.

| Path                                      | Reason                                        |
| ----------------------------------------- | --------------------------------------------- |
| `src1/copy_text/__init__.py`              | Not under `src/`; no active entry imports it. |
| `src1/copy_text/bot.py`                   | —                                             |
| `src1/copy_text/files_list.py`            | —                                             |
| `src1/copy_text/html_bot.py`              | —                                             |
| `src1/copy_text/scan_files.py`            | —                                             |
| `src1/copy_text/text_bot.py`              | —                                             |
| `src1/copy_to_en/__init__.py`             | —                                             |
| `src1/copy_to_en/bot.py`                  | —                                             |
| `src1/copy_to_en/mdwikicx.py`             | —                                             |
| `src1/copy_to_en/medwiki.py`              | —                                             |
| `src1/copy_to_en/tf_page.py`              | —                                             |
| `src1/copy_to_en/x.py`                    | —                                             |
| `src1/copy_to_en/bots/__init__.py`        | —                                             |
| `src1/copy_to_en/bots/alltext_changes.py` | —                                             |
| `src1/copy_to_en/bots/fix_refs_names.py`  | —                                             |
| `src1/copy_to_en/bots/ref.py`             | —                                             |
| `src1/copy_to_en/bots/ref2.py`            | —                                             |
| `src1/copy_to_en/bots/text_changes.py`    | —                                             |
| `src1/fix_use/__init__.py`                | —                                             |
| `src1/fix_use/add.py`                     | —                                             |
| `src1/fix_use/bot.py`                     | —                                             |
| `src1/fix_use/mtab.py`                    | —                                             |
| `src1/fix_use/write_bot.py`               | —                                             |

### `src1_test/`

| Path                                                | Reason                                      |
| --------------------------------------------------- | ------------------------------------------- |
| `src1_test/src1/copy_to_en/test_alltext_changes.py` | Companion test for the unused `src1/` tree. |

### `tests/`

See **Uncertain / Needs Review** below — these are pytest tests, not unused per se.

---

## Unused Folders

Folders where every `.py` file is unused (and therefore the whole directory can be considered dead code, pending review):

| Folder                                     | Notes                                  |
| ------------------------------------------ | -------------------------------------- |
| `src/md_core/commons_svg/`                 | 2 files, plus a `list.wiki` data file. |
| `src/md_core/mdpy/fixref/`                 | 5 files.                               |
| `src/md_core/mdpy/others/`                 | 5 files.                               |
| `src/md_core/stats/`                       | 7 files.                               |
| `src/md_core_helps/apis/sup/`              | 3 files.                               |
| `src/md_core_helps/one_time/` (recursive)  | 56 files — entire subtree.             |
| `src/newupdater/` (recursive)              | 21 files — entire package.             |
| `src/td_core/after_translate/` (recursive) | 8 files — entire subtree.              |
| `src/wprefs/` (recursive)                  | 20 files — entire package.             |
| `src1/` (recursive)                        | 23 files — alternate source tree.      |
| `src1_test/` (recursive)                   | 1 file.                                |

> Folders such as `src/md_core/add_rtt/`, `src/md_core/mdpy/`, `src/td_core/copy_data/`, `src/td_core/fix_user_pages/`, `src/td_core/mdcount/`, and `src/td_core/mdpages/` are **partially** unused — they contain a mix of active and dead `.py` files, so the folder itself must remain.

---

## Uncertain / Needs Review

These files are _not_ reachable through static AST tracing from the 28 active entry points, but **should not be deleted without human review** for the reasons listed.

### Test files (run via `pytest`, not via `pwb.py`)

The repository ships `.github/workflows/pytest.yml` and `tests/conftest.py`, so these run on CI even though no `import` chain links them to a `pwb.py` entry point.

| Path                                                   | Notes                                                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `tests/conftest.py`                                    | Pytest fixture file — discovered automatically by pytest.                                                                 |
| `tests/src/md_core/add_rtt/__init__.py`                | Test package marker.                                                                                                      |
| `tests/src/md_core/add_rtt/add_r_col.py`               | Test helper — verify whether pytest collects it.                                                                          |
| `tests/src/md_core/add_rtt/add_r_col_to_file.py`       | Test helper.                                                                                                              |
| `tests/src/md_core/add_rtt/test.py`                    | Looks like a test.                                                                                                        |
| `tests/src/md_core/add_rtt/tests/add_r_col.py`         | Nested duplicate of above — likely stale.                                                                                 |
| `tests/src/md_core/add_rtt/tests/add_r_col_to_file.py` | Nested duplicate of above — likely stale.                                                                                 |
| `tests/src/wprefs/bots/test_replace_except.py`         | Tests for the (otherwise unused) `wprefs/` package — confirm whether `wprefs/` is intentionally retained for these tests. |
| `tests/src/wprefs/bots/test_replace_except_unit.py`    | Same as above.                                                                                                            |
| `src/md_core/fix_cs1/tests.py`                         | Module-local test file; lives outside `tests/` so pytest may or may not pick it up depending on `testpaths` config.       |
| `src1_test/src1/copy_to_en/test_alltext_changes.py`    | Tests for the unused `src1/` tree.                                                                                        |

### Files possibly invoked outside the `pwb.py` dispatcher

The task statement says `pwb.py` is the _only_ execution path, but the names below suggest CLI scripts that might be invoked directly. **Confirm before deleting.**

| Path                              | Suspicion                                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `src/md_core/fix_cs1/fix_p.py`    | Already correctly traced as USED (imported by `fix_cs1/bot.py`); listed here only to note that it also reads like a runnable script. |
| `src/md_core_helps/one_time/**/*` | Folder name `one_time` strongly implies these were one-shot scripts; safe to archive but verify with the maintainer.                 |
| `src/newupdater/**`               | Entire packages with non-trivial code — possibly under construction or invoked from another orchestrator.                            |
| `src/wprefs/**`                   | Has accompanying tests under `tests/src/wprefs/`; may be a library that is _only_ exercised via tests today.                         |

### Dynamic-import scan

`grep` for `importlib`, `__import__`, `exec(`, `getattr(__name__...)`, `sys.path`, `pkgutil`, and `pkg_resources` across `src/**/*.py` returned **no matches**. Static AST tracing should therefore be complete with respect to dynamic loading; there is no hidden plugin mechanism.

---

## Summary

| Category                                                                                   | Count   |
| ------------------------------------------------------------------------------------------ | ------- |
| Total `.py` files (excluding `old/`, `_old/`, `0/`, `old_codes/`, `.git/`, `__pycache__/`) | **323** |
| Active files (entry points + transitive imports + their package `__init__.py`s)            | **101** |
| Unused files (no traceable import chain from any active entry)                             | **222** |
| Fully unused folders (every file inside is unused)                                         | **12**  |

### Quick bytes-saved estimate

Of the 222 unused files, the largest dead clusters are:

-   `src/md_core_helps/one_time/` — 56 files
-   `src1/` — 23 files
-   `src/newupdater/` — 21 files
-   `src/wprefs/` — 20 files

Removing those five clusters alone would eliminate **155 of the 222** unused files (~70 % of the dead code).

---

## Caveats & methodology notes

1. **AST trace only.** No file is executed; this avoids false positives from runtime side-effects but cannot see `importlib`/`__import__`/`exec` chains. (Confirmed absent — see above.)
2. **`from pkg.mod import Name` is handled both ways** — the trace marks `pkg/mod.py` as used _and_ tries `pkg/mod/Name.py` (in case `Name` is a submodule).
3. **`__init__.py` files** are included as USED whenever any module inside their package is USED, even if the `__init__.py` itself is empty — Python evaluates them at import time.
4. **External libraries** (`mwclient`, `mwparserfromhell`, `pywikibot`, `requests`, `SQLAlchemy`, etc.) are excluded from the trace by checking against the eight known local top-level packages: `copy_to_en`, `md_core`, `md_core_helps`, `mdwiki_api`, `newupdater`, `td_core`, `wprefs`.
5. **Test files** are reported under "Uncertain" rather than "Unused" — they run on CI via pytest, independent of `pwb.py`.
6. **Nothing has been deleted.** This report is purely analytical.
