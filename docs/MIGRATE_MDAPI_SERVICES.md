# Migration Plan: `mdapi_sql/services` → `tools/services` (SQLAlchemy)

## Goal

Replace the legacy `src/db/mdapi_sql/services/` package (raw pymysql) with the existing `src/db/tools/services/` package (SQLAlchemy ORM). All 31+ consumers must be updated and the old package removed.

---

## Current State

### Old (to be removed)

```
src/db/mdapi_sql/services/
  __init__.py              (empty)
  sql_for_mdwiki.py        # 187 lines — raw SQL wrappers
  sql_qids.py              # 147 lines — qids table via pymysql
  sql_qids_others.py       # 147 lines — qids_others table via pymysql
```

### New (already exists)

```
src/db/tools/
  models/                   # 19 ORM models (QidRecord, PageRecord, CategoryMemberRecord, UserRecord, …)
  services/
    session.py              # SQLAlchemy engine + sessionmaker + get_session()
    user_service.py         # UserRecord CRUD (already exists)
    delete_service.py       # Generic PK-based deletion
    wikidata/
      qid_service.py        # QidRecord CRUD
      qid_others_service.py # QidOthersRecord CRUD
      allqid_service.py
    pages/
      page_service.py       # PageRecord CRUD + add_translate_row_to_db
      user_page_service.py
      in_process_service.py
      pages_users_to_main_service.py
      missing_stats_service.py
      results_2026_service.py
      translate_type_service.py
    analytics/
      refs_count_service.py
      assessment_service.py
      word_service.py
      enwiki_pageview_service.py
      mdwiki_revid_service.py
      views_new_service.py
    content/
      category_service.py
      lang_service.py
      project_service.py
    reports/
      pages_users_to_main_service.py
```

### Consumers of old services: **31+ files** across:

-   `copy_to_en/` (1)
-   `wprefs/` (1)
-   `td_core/fix_user_pages/` (4)
-   `td_core/mdpyget/` (4)
-   `td_core/after_translate/` (4)
-   `td_core/copy_data/` (8)
-   `td_core/db_work/` (2)
-   `td_core/mdcount/` (3)
-   `td_core/mdpages/` (4)
-   `td_core/td_other_qids/` (2)
-   `td_core/wd_works/` (1)
-   `md_core/` (3)
-   `md_core/p11143_bot/` (1)
-   `md_core_helps/` (2)

---

## Phase 1: Fill Gaps in the New System

### 1.1 Batch QID operations — extend `qid_service.py`

| Old function                                           | New function                                       |
| ------------------------------------------------------ | -------------------------------------------------- |
| `set_qid_where_qid(new_qid, old_qid)`                  | `update_qid_by_value(old_qid, new_qid)`            |
| `set_qid_where_title(title, qid)`                      | `update_qid_by_title(title, qid)`                  |
| `delete_title_from_db(title, pr)`                      | `delete_by_title(title)`                           |
| `set_title_where_qid(new_title, qid)`                  | `update_title_by_qid(qid, new_title)`              |
| `qids_set_title_where_title_qid(old, new, qid, no_do)` | `update_title_conditionally(old, new, qid, no_do)` |
| `add_titles_to_qids(tab0, add_empty_qid)`              | `batch_upsert_qids(tab0, add_empty_qid)`           |

Same set for `qid_others_service.py`.

### 1.2 Create `category_member_service.py` — new file

| Old function                                                 | New function                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| `get_db_category_members()` → `dict[cat → list[article_id]]` | `get_all_category_members()` → `dict[str, list[str]]`         |
| `select DISTINCT article_id from category_members`           | `list_distinct_article_ids()` → `list[str]`                   |
| `all_articles.py` diff-and-insert logic                      | `batch_sync_category_members(data: list[dict])` → bulk upsert |

Location: `src/db/tools/services/content/category_member_service.py`

### 1.3 Add missing convenience functions

| Gap                                                              | Solution                                                                        |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `sql_for_mdwiki.get_all_pages()` → `list[str]` titles            | Add `list_page_titles()` to `page_service.py`                                   |
| `sql_for_mdwiki.get_db_categories()` → `dict[str, int]`          | Add `list_categories_as_dict()` to `category_service.py`                        |
| `sql_for_mdwiki.get_all_from_table(table)` → dynamic table query | No direct replacement — each caller migrates to the appropriate typed ORM query |
| `sql_for_mdwiki.set_deleted_where_id(iid)`                       | Callers use `page_service.update_page(page_id, deleted=1)` directly             |

---

## Phase 2: Rewrite `src/db/utils/to_sql.py` with SQLAlchemy

`to_sql.py` provides 6 generic functions that currently use `sql_for_mdwiki.mdwiki_sql()`:

| Function                                                            | Strategy                                                                                  |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `mdwiki_sql_one_table(table, columns, all_data, operation)`         | Use `inspect(engine)` → `Table` reflection → `session.execute(insert(Table).values(...))` |
| `insert_dict(data, table_name, operation)`                          | Reflect table, build INSERT via ORM `Table` object                                        |
| `update_table(conn, tab, col_name, col_value, col_set, values_set)` | Reflect table, build UPDATE via `update(Table)`                                           |
| `update_table_2(...)`                                               | Same as above                                                                             |
| `to_sql(table_name, columns, all_data, operation)`                  | Bulk INSERT via `session.execute(insert(Table), list_of_dicts)`                           |
| `new_to_sql(table_name, columns, all_data)`                         | Bulk INSERT same way                                                                      |

**Key technique:** Use SQLAlchemy's `Table` reflection to dynamically map table names to ORM objects without hardcoding every model.

---

## Phase 3: Update All 31+ Consumers

### Pattern: imports

```python
# OLD
from db.mdapi_sql.services import sql_for_mdwiki
from db.mdapi_sql.services import sql_qids
from db.mdapi_sql.services import sql_qids_others

# NEW
from db.tools.services.session import get_session
from db.tools.services.pages.page_service import list_page_titles, add_translate_row_to_db
from db.tools.services.wikidata.qid_service import get_title_to_qid, add_qid, update_qid_by_title, …
from db.tools.services.wikidata.qid_others_service import get_title_to_qid, add_qid_other, …
```

### File-by-file migration map

| File                                               | Old function(s) → New function(s)                                                                  |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `src/copy_to_en/revid.py`                          | `mdwiki_sql` → ORM query                                                                           |
| `src/wprefs/bot.py`                                | `mdwiki_sql` → ORM / `text()`                                                                      |
| `td_core/fix_user_pages/bot.py`                    | `get_db_users()` → `user_service.list_usernames()`                                                 |
| `td_core/fix_user_pages/user_bot.py`               | `get_db_users()` → `user_service.list_usernames()`                                                 |
| `td_core/fix_user_pages/fix_it_db.py`              | `mdwiki_sql` → ORM                                                                                 |
| `td_core/fix_user_pages/fix_it_db_new.py`          | `mdwiki_sql` → ORM                                                                                 |
| `td_core/fix_user_pages/del.py`                    | `mdwiki_sql` → ORM                                                                                 |
| `td_core/mdpyget/sqlviews_new.py`                  | `select_md_sql` → ORM query                                                                        |
| `td_core/mdpyget/pages_list.py`                    | `select_md_sql` → ORM query                                                                        |
| `td_core/mdpyget/getas.py`                         | `select_md_sql` → ORM query                                                                        |
| `td_core/mdpyget/enwiki_views.py`                  | `select_md_sql` → ORM query                                                                        |
| `td_core/after_translate/fixcat.py`                | `mdwiki_sql` → ORM                                                                                 |
| `td_core/after_translate/get_pages.py`             | `get_all_pages_all_keys` → `page_service.list_pages()`                                             |
| `td_core/after_translate/add_to_pages_users_db.py` | `mdwiki_sql` → ORM                                                                                 |
| `td_core/after_translate/add_to_mdwiki.py`         | `mdwiki_sql` → ORM                                                                                 |
| `td_core/copy_data/copy_word_table.py`             | `mdwiki_sql` → ORM / `word_service`                                                                |
| `td_core/copy_data/copy_assessments.py`            | `mdwiki_sql` → ORM / `assessment_service`                                                          |
| `td_core/copy_data/copy_word_2.py`                 | `mdwiki_sql` → ORM / `word_service`                                                                |
| `td_core/copy_data/copy_refs_2.py`                 | `mdwiki_sql` → ORM / `refs_count_service`                                                          |
| `td_core/copy_data/copy_enwiki_pageviews.py`       | `mdwiki_sql` → ORM / `enwiki_pageview_service`                                                     |
| `td_core/copy_data/by_title/all_articles.py`       | `get_db_category_members()` + `mdwiki_sql` → `category_member_service`                             |
| `td_core/copy_data/by_qid/sitelinks.py`            | `sql_qids.get_all_qids()` + `sql_qids_others.get_others_qids()` → `qid_service.get_title_to_qid()` |
| `td_core/db_work/days_7.py`                        | `mdwiki_sql` → ORM                                                                                 |
| `td_core/db_work/check_titles.py`                  | `mdwiki_sql` → ORM                                                                                 |
| `td_core/mdcount/countrefs_and_words.py`           | `select_md_sql` + `get_db_category_members` → `category_member_service`                            |
| `td_core/mdcount/words.py`                         | `select_md_sql` → ORM                                                                              |
| `td_core/mdcount/countref.py`                      | `select_md_sql` → ORM                                                                              |
| `td_core/mdpages/cashwd.py`                        | `mdwiki_sql` → ORM                                                                                 |
| `td_core/mdpages/find_qids.py`                     | `sql_qids.*` → `qid_service.*`                                                                     |
| `td_core/mdpages/create_qids.py`                   | `sql_qids.*` → `qid_service.*`                                                                     |
| `td_core/mdpages/find_mt.py`                       | `sql_qids_others.*` → `qid_others_service.*`                                                       |
| `td_core/td_other_qids/make_list.py`               | `sql_qids.get_all_qids()` → `qid_service.get_title_to_qid()`                                       |
| `td_core/td_other_qids/fix_qids.py`                | `sql_qids.set_qid_where_title()` → `qid_service.update_qid_by_title()`                             |
| `td_core/wd_works/recheck.py`                      | `sql_qids.*` → `qid_service.*`                                                                     |
| `md_core/mdpy/orred.py`                            | `mdwiki_sql` → ORM                                                                                 |
| `md_core/mdpy/others/copy_qids.py`                 | `sql_qids.*` → `qid_service.*`                                                                     |
| `md_core/unlinked_wb/hlps.py`                      | `sql_qids.*` + `sql_qids_others.*` → `qid_service.*` + `qid_others_service.*`                      |
| `md_core/p11143_bot/bot.py`                        | `sql_qids.*` + `sql_qids_others.*` → `qid_service.*` + `qid_others_service.*`                      |
| `md_core_helps/apis/cat_cach.py`                   | `mdwiki_sql` → ORM                                                                                 |
| `md_core_helps/bots/en_to_md.py`                   | `sql_qids.*` → `qid_service.*`                                                                     |

---

## Phase 4: Cleanup

| Task                                  | Details                                 |
| ------------------------------------- | --------------------------------------- |
| Delete `src/db/mdapi_sql/services/`   | Entire directory (4 files)              |
| Update `src/db/__init__.py`           | Wire up new service exports, remove old |
| Update `src/db/mdapi_sql/__init__.py` | Remove any service imports              |
| Run `ruff check . --fix`              | Auto-fix formatting issues              |
| Run `mypy .`                          | Verify type correctness                 |
| Run `pytest`                          | Ensure no regressions                   |

---

## Migration Map (summary table)

| Old module                                              | New module(s)                                                        |
| ------------------------------------------------------- | -------------------------------------------------------------------- |
| `sql_for_mdwiki.get_all_pages()` → `list[str]`          | `page_service.list_page_titles()` (new)                              |
| `sql_for_mdwiki.get_db_categories()` → `dict[str, int]` | `category_service.list_categories_as_dict()` (new)                   |
| `sql_for_mdwiki.get_db_category_members()`              | `category_member_service.get_all_category_members()` (new)           |
| `sql_for_mdwiki.get_db_users()` → `list[str]`           | `user_service.list_usernames()` (new) or `user_service.list_users()` |
| `sql_for_mdwiki.set_target_where_id(target, id)`        | `page_service.set_page_target(record, target)`                       |
| `sql_for_mdwiki.insert_to_pages_users_to_main(...)`     | `reports.pages_users_to_main_service.add_pages_users_to_main(...)`   |
| `sql_for_mdwiki.add_new_to_pages(tab)`                  | `page_service.add_translate_row_to_db(...)`                          |
| `sql_for_mdwiki.set_deleted_where_id(id)`               | `page_service.update_page(page_id, deleted=1)`                       |
| `sql_qids.get_all_qids()` → `{title: qid}`              | `qid_service.get_title_to_qid()`                                     |
| `sql_qids.add_qid(title, qid)`                          | `qid_service.add_qid(title, qid)`                                    |
| `sql_qids.set_qid_where_qid(new, old)`                  | `qid_service.update_qid_by_value(old, new)` (new)                    |
| `sql_qids.set_qid_where_title(title, qid)`              | `qid_service.update_qid_by_title(title, qid)` (new)                  |
| `sql_qids.delete_title_from_db(title, pr)`              | `qid_service.delete_by_title(title)` (new)                           |
| `sql_qids.set_title_where_qid(title, qid)`              | `qid_service.update_title_by_qid(qid, title)` (new)                  |
| `sql_qids.qids_set_title_where_title_qid(...)`          | `qid_service.update_title_conditionally(...)` (new)                  |
| `sql_qids.add_titles_to_qids(tab, empty)`               | `qid_service.batch_upsert_qids(tab, empty)` (new)                    |
| (same 6 functions for qids_others)                      | `qid_others_service.*` (new equivalents)                             |
| `to_sql.py` (6 generic functions)                       | SQLAlchemy `Table` reflection + bulk operations                      |

---

## Estimated Work Items

| Area                            | Files to touch           | Complexity           |
| ------------------------------- | ------------------------ | -------------------- |
| New service functions (Phase 1) | 4 files to extend/create | Medium               |
| `to_sql.py` rewrite (Phase 2)   | 1 file                   | High (generic logic) |
| Consumer updates (Phase 3)      | 31 files                 | High (many callers)  |
| Cleanup (Phase 4)               | 3–4 files                | Low                  |
| **Total**                       | **~39 files**            |                      |

---

## Key Risks

1. **Different DB URL configuration** — old system uses `DB_NAME` env var (default `{user}__mdwiki`), new system uses `TOOL_TOOLSDB_DBNAME` (default `s57081__svgdb`). Must ensure all consumers point to the same database after migration.
2. **`to_sql.py`** is the riskiest piece — generic table operations require careful testing.
3. **No existing tests** for any DB layer — manual verification or ad-hoc testing needed.
4. **`users` table** has columns (`email`, `wiki`, `user_group`, `created_at`) that the old code never uses — the new `UserRecord` model includes them. Must ensure inserts don't break on NOT NULL columns without defaults (check server_default).

---

## Recommended Execution Order

1. Phase 1 (fill gaps) — add all missing service functions
2. Phase 2 (to_sql.py) — rewrite with SQLAlchemy reflection
3. Phase 3 (consumers) — update one group at a time, verify after each:
    - Start with `copy_data/` (heaviest users of raw SQL)
    - Then `td_other_qids/` + `mdpages/` (qid operations — well-covered by new services)
    - Then `md_core/` + `md_core_helps/`
    - Then `fix_user_pages/` and remaining
4. Phase 4 (cleanup) — delete old package and finalize
