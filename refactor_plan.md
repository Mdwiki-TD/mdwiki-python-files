# Refactor Plan: Lazy Loading for Module-Level Expensive Operations

## Summary

This project has **~50+ locations** where API calls, database queries, file I/O, or heavy computations execute at **module import time**. This causes slow startup, wasted resources when only utility functions are needed, and cascading import chains.

Below is a prioritized plan organized by pattern type, with old code → new code for each case.

---

## Priority 3: Database Queries at Module Level (12 files)

### Pattern: `variable = sql_for_mdwiki.get_db_categories()`

Affected files doing `get_db_categories()`:

| #   | File                         | Line | Old Code                                           | Used In                           |
| --- | ---------------------------- | ---- | -------------------------------------------------- | --------------------------------- |
| 1   | `src/copy_text/text_bot.py`  | 18   | `mdwiki_cats = sql_for_mdwiki.get_db_categories()` | `get_cats()` — iterates dict keys |
| 2   | `src/copy_to_en/medwiki.py`  | 37   | `mdwiki_cats = sql_for_mdwiki.get_db_categories()` | `get_cats()` — iterates dict keys |
| 3   | `src/copy_to_en/mdwikicx.py` | 37   | `mdwiki_cats = sql_for_mdwiki.get_db_categories()` | `get_cats()` — iterates dict keys |

**New code for all three:**

```python
@functools.lru_cache(maxsize=1)
def get_mdwiki_cats():
    return sql_for_mdwiki.get_db_categories()
```

Replace `for category in mdwiki_cats` with `for category in get_mdwiki_cats()`.

### Pattern: `variable = sql_for_mdwiki.select_md_sql(...)`

| #   | File                        | Line  | Old Code                                                            | Notes                                                                |
| --- | --------------------------- | ----- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 4   | `src/copy_text/text_bot.py` | 20-24 | `full_translate = sql_for_mdwiki.select_md_sql(...)` then list comp | Used in `get_text()` — membership test `x.strip() in full_translate` |

```python
@functools.lru_cache(maxsize=1)
def get_full_translate():
    data = sql_for_mdwiki.select_md_sql(
        "select DISTINCT tt_title from translate_type where tt_full = 1;", return_dict=True
    )
    return [ta["tt_title"] for ta in data]
```

### Pattern: `variable = sql_qids.get_all_qids()`

| #   | File                                   | Line  | Old Code                                                                          | Notes                               |
| --- | -------------------------------------- | ----- | --------------------------------------------------------------------------------- | ----------------------------------- |
| 5   | `src/md_core/mdpy/bots/en_to_md.py`    | 35    | `mdtitle_to_qid = sql_qids.get_all_qids()`                                        | Used as dict mapping `{title: qid}` |
| 6   | `src/td_core/db_work/get_red.py`       | 19-20 | Two DB queries: `qids_title_to_qid` and `qids_others_title_to_qid`                | `.get(old_title)` dict lookups      |
| 7   | `src/td_core/mdpages/find_qids.py`     | 24-30 | `qids = sql_qids.get_all_qids()` + two derived variables `qids_already`, `noqids` | `.items()`, `.get()`, `len()`       |
| 8   | `src/md_core/mdpy/others/copy_qids.py` | 19    | `in_qids = sql_qids.get_all_qids()`                                               | `.get(title)`, `title in in_qids`   |

**For file #7 (`find_qids.py`)**, `qids_already` and `noqids` are derived from `qids` at module level too. Need to wrap all three:

```python
@functools.lru_cache(maxsize=1)
def get_qids():
    return sql_qids.get_all_qids()

@functools.lru_cache(maxsize=1)
def get_qids_already():
    qids = get_qids()
    return {q: title for title, q in qids.items() if q != ""}

@functools.lru_cache(maxsize=1)
def get_noqids():
    qids = get_qids()
    return [title for title, q in qids.items() if q == "" and valid_title(title)]
```

**⚠️ Warning:** `noqids` uses `valid_title()` which itself may import modules. Check for circular import.

### Pattern: Other large DB fetches

| #   | File                                                        | Line   | Old Code                                                                                                 | Approach                                                        |
| --- | ----------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 9   | `src/td_core/fix_user_pages/bot.py`                         | 30, 38 | `db_users = sql_for_mdwiki.get_db_users()` + `already_in_db = sql_for_mdwiki.get_all_from_table(...)`    | Wrap both in cached functions                                   |
| 10  | `src/td_core/fix_user_pages/user_bot.py`                    | 12     | `db_users = sql_for_mdwiki.get_db_users()`                                                               | Wrap in cached function                                         |
| 11  | `src/td_core/after_translate/bots/add_to_pages_users_db.py` | 27-40  | `pages_users = sql_for_mdwiki.get_all_pages_all_keys(...)` + module-level for-loop building nested dict  | Wrap entire block in cached function                            |
| 12  | `src/td_core/fix_user_pages/fix_it_db.py`                   | 15-16  | `all_infos = sql_for_mdwiki.get_all_from_table(...)` + dict comp                                         | Wrap in cached function                                         |
| 13  | `src/td_core/copy_data/by_qid/sitelinks.py`                 | 37-45  | `db_data_main = sql_for_mdwiki.select_md_sql(...)` + module-level for-loop building `in_sql_qid_targets` | Wrap in cached function                                         |
| 14  | `src/md_core/mdpy/wddone.py`                                | 22-47  | `sq = sql_for_mdwiki.select_md_sql(...)` + entire module-level for-loop with INSERT queries              | This is a **script** — move all module-level code into `main()` |
| 15  | `src/td_core/after_translate/bots/add_to_wd.py`             | 43-55  | `sq_dd = sql_for_mdwiki.select_md_sql(...)` + module-level for-loop building lookup lists                | Wrap in cached function                                         |

---

## Priority 4: File I/O at Module Level (10 files)

### Pattern: `json.load(open(...))` on import

All in `src/md_core_helps/one_time/` and related dirs:

| #   | File                                                                     | Line   | Variable                                  | File Read                          |
| --- | ------------------------------------------------------------------------ | ------ | ----------------------------------------- | ---------------------------------- |
| 1   | `src/md_core_helps/one_time/niosh/get.py`                                | 28, 30 | `data`, `boths`                           | `cite_file.json`, `both_file.json` |
| 2   | `src/md_core_helps/one_time/priorviews/lists/views.py`                   | 36     | `ViewsData`                               | `views_mdwiki_langs.json`          |
| 3   | `src/md_core_helps/one_time/priorviews/lists/words.py`                   | 28     | `words_by_lang`                           | `words_mdwiki_langs.json`          |
| 4   | `src/md_core_helps/one_time/priorviews/lists/translators.py`             | 31     | `tra_by_lang`                             | `translators_mdwiki_langs.json`    |
| 5   | `src/md_core_helps/one_time/priorviews/lists/links_by_section.py`        | 31, 47 | `all_pages_states`, `sections_links`      | `all_pages_states.json`, sections  |
| 6   | `src/md_core_helps/one_time/priorviews/lists/creators.py`                | 34, 42 | `creators_as_translators`, `CreatorsData` | Two JSON files                     |
| 7   | `src/md_core_helps/one_time/priorviews/lists/creators_to_translators.py` | 35     | `creators_as_translators`                 | `creators_as_translators.json`     |
| 8   | `src/md_core_helps/one_time/priorviews/bots/sections_links.py`           | 32     | `old`                                     | `secs_links.json`                  |
| 9   | `src/md_core_helps/one_time/priorviews/find/find_blame.py`               | 52     | `new_data`                                | `blames.json`                      |
| 10  | `src/md_core_helps/one_time/priorviews/find/find_creator.py`             | 35     | `CreatorsData`                            | `creators_by_lang.json`            |

**Common fix pattern:**

```python
@functools.lru_cache(maxsize=1)
def get_views_data():
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)
```

**⚠️ Warning for `priorviews/` files:** These files import from each other. For example, `by_lang.py` and `langs.py` import variables from `views.py`, `words.py`, etc. Those cascading imports trigger all the `json.load()` calls. Fixing one cascades. Safest approach: wrap each JSON load in its own module-level lazy function, and update cross-module imports to call the function instead of accessing the variable.

**For `by_lang.py` (line 30-65) and `langs.py` (line 37-41):** These also do **heavy computation** on module-level data. Move computation inside lazy functions too.

---

## Priority 5: Full Script Execution at Module Level (5 files)

These files execute their entire logic on import because there's no `__main__` guard:

| #   | File                                    | Problem                                                              |
| --- | --------------------------------------- | -------------------------------------------------------------------- |
| 1   | `src/md_core/updates/c2023.py`          | Entire data pipeline runs on import — API calls, loops, page saves   |
| 2   | `src/md_core/updates/listo.py`          | API calls `Get_All_pages`, `GetPageText`, `CatDepth` at module level |
| 3   | `src/md_core/updates/io.py`             | File read + API calls + heavy loop with API calls per page           |
| 4   | `src/copy_to_en/x.py`                   | `cat_cach.from_cache()` API call + HTTP requests loop                |
| 5   | `src/td_core/td_other_qids/fix_qids.py` | `cat_cach.from_cache()` API call + list comp                         |

**Fix for all:** Wrap all module-level code in a `main()` function, add `if __name__ == "__main__": main()` at the end.

---

## Priority 6: Minor / Environment Reads

| #   | File                                    | Line | Notes                                                                  |
| --- | --------------------------------------- | ---- | ---------------------------------------------------------------------- |
| 1   | `src/md_core_helps/mdapi_sql/sql_qu.py` | 20   | `os.getenv()` only — cheap, optional to refactor                       |
| 3   | `src/td_core/mdpyget/sqlviews_new.py`   | 20   | `PageviewsClient()` — lightweight client init, no network until called |

These are low priority and can stay as-is.

---

## Cross-Cutting Concerns

### 1. `newapi` module is an external dependency

The `newapi` library is not in this repo — it's installed in the Python path. The `AllAPIS` object authenticates when created (network call). Wrapping in `lru_cache` ensures it authenticates only once.

### 2. `CatDepth` usage already lazy in `wiki_page.py`

In `src/mdwiki_api/wiki_page.py:54`, `CatDepth()` is already a function that calls `load_main_api()` internally — good. But `load_main_api()` itself runs module-level env reads (lines 16-17). These are cheap env reads and can stay.

### 3. `src/md_core_helps/apis/mdwiki_api_call.py` is the most critical wrapper

It's used by `copy_text/text_bot.py`, `copy_to_en/medwiki.py`, `copy_to_en/mdwikicx.py`, and others. Any refactoring here must:

-   Not break `from md_core_helps.apis.mdwiki_api_call import post_s, page_put`
-   Consider backward compat for `api_new` if anything directly imports it

### 4. Circular import risk

Check dependencies:

-   `md_core_helps/apis/` imports from `mdwiki_api/`
-   `md_core_helps/mdapi_sql/` imports from `md_core_helps/apis/`? Let's verify.
-   `copy_text/text_bot.py` imports from both `md_core_helps/apis/` and `md_core_helps/mdapi_sql/`

Since we're wrapping DB queries in lazy functions (not importing them eagerly), circular import risk should actually decrease.

### 5. Shared mutable state

Some module-level variables are **dicts that get mutated**:

-   `text_cache`, `revid_cache`, `un_wb_tag_cache` in `text_bot.py` and `medwiki.py` — these are caches, safe to keep as-is
-   `qids_all`, `to_set`, `new_tabs_to_db` in `fix_user_pages/bot.py` — these are module-level accumulators, sketchy pattern. Should be local to functions
-   `mis_qids` in `sitelinks.py` (line 32) — mutated by `wbgetentities()`. Should be function-local

These mutable globals are a separate code smell but not part of this refactor scope.

### 6. `__main__` guards

Some files have `if __name__ == "__main__": main()` but still do expensive work at module level BEFORE that guard (e.g., `bot.py` files with module-level `api_new = NewApi(...)`). In those cases, the `__main__` guard only wraps the "main logic" but the import-time cost is still paid. Lazy wrapping solves this.

---

## Refactoring Implementation Strategy

### Phase 1: Fix the root cause

1. `src/mdwiki_api/mdwiki_page.py` — make `NewApi`, `MainPage`, `CatDepth` lazy functions
2. `src/mdwiki_api/wiki_page.py` — verify `load_main_api` is already cached (it is) and env reads are cheap (they are)

### Phase 2: Fix `mdwiki_api_call.py`

3. Replace module-level `api_new` with lazy getter
4. Update all internal functions to use the getter

### Phase 3: Fix all direct `NewApi(...)` callers

5-21. Each file with `api_new = NewApi(...)` at module level

### Phase 4: Fix database query modules

22-36. Each file with DB queries at module level

### Phase 5: Fix file I/O modules

37-46. Each file with `json.load(open(...))` at module level

### Phase 6: Fix scripts without `__main__` guards

47-51. Add `main()` + `if __name__ == "__main__"` guards

### Verification

After each phase, run:

```bash
pytest
ruff check .
mypy .
```
