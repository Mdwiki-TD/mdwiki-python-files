# Plan: Contain `get_session` Inside the `db` Package

## Goal

Restrict direct usage of `get_session()` (and `SessionLocal`, `engine`) to files
inside `src/db/` only.  Outside code must go through the typed service layer
(`db.tools.services.*`).

---

## Current State

### Inside `db/` (25 files — correct usage)

All service modules in `db/tools/services/` import via relative paths
(e.g. `from ..session import get_session`).  These are fine and stay as-is.

### Outside `db/` (27 files — must be eliminated)

All 27 import `get_session` from `db.tools.services.session` and use it for
raw `text()` queries:

| # | File | SQL patterns used |
|---|---|---|
| 1 | `wprefs/bot.py` | `SELECT DISTINCT title, qid FROM qids` |
| 2 | `md_core/mdpy/orred.py` | `SELECT title, target FROM pages WHERE …` |
| 3 | `md_core/mdpy/others/copy_qids.py` | `SELECT title, qid FROM qids` |
| 4 | `td_core/wd_works/recheck.py` | Various qid queries |
| 5 | `td_core/mdpyget/sqlviews_new.py` | `views_new` SELECT/INSERT/UPDATE |
| 6 | `td_core/mdpyget/getas.py` | `assessments` SELECT |
| 7 | `td_core/mdpyget/enwiki_views.py` | `enwiki_pageviews` SELECT |
| 8 | `td_core/mdcount/words.py` | `words` SELECT |
| 9 | `td_core/mdcount/countref.py` | `refs_counts` SELECT |
| 10 | `td_core/mdcount/countrefs_and_words.py` | `words` + `refs_counts` SELECT |
| 11 | `td_core/mdcount/ref_words_bot.py` | `words` + `refs_counts` SELECT |
| 12 | `td_core/copy_data/copy_word_table.py` | `words` SELECT |
| 13 | `td_core/copy_data/copy_word_2.py` | `words` SELECT |
| 14 | `td_core/copy_data/copy_refs_2.py` | `refs_counts` SELECT |
| 15 | `td_core/copy_data/copy_enwiki_pageviews.py` | `enwiki_pageviews` SELECT |
| 16 | `td_core/copy_data/copy_assessments.py` | `assessments` SELECT |
| 17 | `td_core/copy_data/by_qid/sitelinks.py` | `all_qids_exists` + `qids` SELECT |
| 18 | `td_core/db_work/days_7.py` | `pages` SELECT/UPDATE |
| 19 | `td_core/db_work/check_titles.py` | `pages` + `pages_users` SELECT |
| 20 | `td_core/fix_user_pages/bot.py` | `pages_users_to_main` SELECT |
| 21 | `td_core/fix_user_pages/del.py` | `pages_users_to_main` DEL |
| 22 | `td_core/fix_user_pages/fix_it_db.py` | `words` SELECT + `pages` INSERT/DEL |
| 23 | `td_core/fix_user_pages/fix_it_db_new.py` | `pages_users_to_main` INSERT |
| 24 | `td_core/after_translate/bots/fixcat.py` | `pages` UPDATE |
| 25 | `td_core/after_translate/bots/add_to_pages_users_db.py` | `pages_users` + `pages` SELECT |
| 26 | `td_core/after_translate/bots/add_to_mdwiki.py` | `pages` SELECT |
| 27 | `td_core/after_translate/bots/get_pages.py` | `pages` + `pages_users` SELECT |

---

## Strategy

Follow a **bottom-up** approach:

1. **Identify raw SQL patterns** used by each file (simple SELECT, INSERT,
   UPDATE, DELETE on known tables).
2. **Add new service functions** to the appropriate existing service module
   (or create a thin utility service) that wraps each pattern as a typed
   function taking simple parameters and returning simple results.
3. **Replace** each external `get_session()` + `text()` call with a call to
   the new service function.
4. **Verify** the final state: zero `get_session` imports remain outside `db/`.

---

## Phase 1: Add Missing Service Functions

### 1.1 Extend `analytics` services

These files all do the same pattern — fetch all rows from an analytics table
into a `dict[key → value]` for in-memory comparison:

| File | Table | Key col | Value col | Current pattern |
|---|---|---|---|---|
| `copy_word_table.py` | `words` | `w_title` | `w_lead_words`, `w_all_words` | `SELECT *` → `dict` |
| `copy_word_2.py` | `words` | `w_title` | `w_lead_words`, `w_all_words` | `SELECT *` → `dict` |
| `copy_refs_2.py` | `refs_counts` | `r_title` | `r_lead_refs`, `r_all_refs` | `SELECT *` → `dict` |
| `copy_enwiki_pageviews.py` | `enwiki_pageviews` | `title` | `en_views` | `SELECT *` → `dict` |
| `copy_assessments.py` | `assessments` | `title` | `importance` | `SELECT *` → `dict` |
| `getas.py` | `assessments` | `title` | `importance` | `SELECT *` → `dict` |
| `enwiki_views.py` | `enwiki_pageviews` | `title` | `en_views` | `SELECT *` → `dict` |
| `words.py` | `words` | `w_title` | lead/all | `SELECT *` → `dict` |
| `countref.py` | `refs_counts` | `r_title` | lead/all | `SELECT *` → `dict` |
| `ref_words_bot.py` | `words`/`refs_counts` | `w_title`/`r_title` | lead/all | `SELECT *` → `dict` |

**Action:** Add `fetch_all_as_dict(table_name, key_col, value_cols)` to a new
generic service `db/tools/services/query_service.py`, or add dict-style
accessors to each existing analytics service.

**Better approach — add convenience functions per service:**

- `word_service.fetch_all_as_dicts()` → `dict[str, dict]`
- `refs_count_service.fetch_all_as_dicts()` → `dict[str, dict]`
- `enwiki_pageview_service.fetch_all_as_dicts()` → `dict[str, dict]`
- `assessment_service.fetch_all_as_dicts()` → `dict[str, dict]`

### 1.2 Extend `views_new_service`

`schema: td_core/mdpyget/sqlviews_new.py` does:

```python
with get_session() as session:
    rows = session.execute(text("SELECT * FROM views_new ...")).fetchall()
    existing = [dict(r._mapping) for r in rows]
```

**Action:** Add `fetch_all_views()` returning `list[dict]` and
`upsert_views(target, lang, year, views)` to `views_new_service.py`.

### 1.3 Extend `user_page_service` / `page_service`

| File | Pattern |
|---|---|
| `fix_it_db.py` | `SELECT w_title, w_lead_words, w_all_words FROM words` + `INSERT INTO pages` + `SELECT from pages` + `DELETE FROM pages_users` |
| `fix_it_db_new.py` | `INSERT INTO pages_users_to_main` + `SELECT from pages_users_to_main` |
| `del.py` | `SELECT from pages_users_to_main` + `DELETE FROM pages_users_to_main` + `DELETE FROM pages_users` |
| `add_to_pages_users_db.py` | `SELECT from pages_users` + `SELECT from pages` |
| `add_to_mdwiki.py` | `SELECT from pages` |
| `get_pages.py` | `SELECT from pages` + `SELECT from pages_users` |
| `orred.py` | `SELECT title, target FROM pages WHERE ...` |
| `days_7.py` | `SELECT from pages` + `UPDATE pages` |
| `check_titles.py` | `SELECT from pages` + `pages_users` |

**Action:** Add missing query methods:
- `page_service.fetch_pages_by_conditions(lang, cat, deleted, ...)` → `list[PageRecord]`
- `page_service.fetch_titles_targets(lang)` → `list[tuple[str, str]]`
- `user_page_service.delete_by_ids(ids: list[int])`
- `pages_users_to_main_service.delete_by_ids(ids: list[int])`

### 1.4 Extend `qid_service` / `qid_others_service`

| File | Pattern |
|---|---|
| `wprefs/bot.py` | `SELECT DISTINCT title, qid FROM qids` |
| `recheck.py` | Various qid lookups |
| `copy_qids.py` | `SELECT title, qid FROM qids` |

These are already covered by existing `get_title_to_qid()` functions.

### 1.5 Extend `category_service`

`add_to_pages_users_db.py` and `get_pages.py` also use category lookups.

---

## Phase 2: Replace All External `get_session` Calls

For each of the 27 files, in groups:

1. **Analytics group** (8 files): `words.py`, `countref.py`, `countrefs_and_words.py`,
   `ref_words_bot.py`, `copy_word_table.py`, `copy_word_2.py`, `copy_refs_2.py`,
   `copy_enwiki_pageviews.py`, `copy_assessments.py`, `getas.py`, `enwiki_views.py`,
   `sqlviews_new.py`

2. **Fix_user_pages group** (4 files): `bot.py`, `del.py`, `fix_it_db.py`,
   `fix_it_db_new.py`

3. **after_translate group** (4 files): `fixcat.py`, `add_to_pages_users_db.py`,
   `add_to_mdwiki.py`, `get_pages.py`

4. **db_work group** (2 files): `days_7.py`, `check_titles.py`

5. **Remaining** (5 files): `wprefs/bot.py`, `orred.py`, `copy_qids.py`,
   `recheck.py`, `sitelinks.py`

### Replacement pattern

```python
# BEFORE
from db.tools.services.session import get_session
from sqlalchemy import text

with get_session() as session:
    rows = session.execute(text("SELECT title, target FROM pages WHERE lang = :l"), {"l": lang}).fetchall()
    result = [dict(r._mapping) for r in rows]

# AFTER
from db.tools.services.pages.page_service import fetch_titles_targets_by_lang

result = fetch_titles_targets_by_lang(lang)
```

---

## Phase 3: Verify

1. Run `grep "from db\.tools\.services\.session import" src/` (outside `src/db/`) → 0 matches.
2. Run `ruff check .` → no regressions.
3. Run a quick import test: `python -c "from db import get_session; ..."` → works.

---

## Summary of Work Items

| Area | New service functions | Files to touch | Complexity |
|---|---|---|---|
| Analytics services | ~8 fetch-all-as-dict functions | 12 files | Low |
| views_new_service | fetch_all_views, upsert_views | 1 file | Low |
| page_service | fetch_pages_by_conditions, fetch_titles_targets_by_lang | ~10 files | Medium |
| user_page_service | delete_by_ids | 3 files | Medium |
| pages_users_to_main | delete_by_ids | 3 files | Medium |
| Verify & cleanup | — | — | Low |

**Total:** ~15 new service functions in 6 service files, updating 27 consumer files.
