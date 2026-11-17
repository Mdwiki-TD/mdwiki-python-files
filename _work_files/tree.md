```
src/
│
├── pybot/
│   │
│   ├── db/
│   │   │
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── maps.py
│   │   │   └── replica_db.py
│   │   │
│   │   ├── mdapi_sql/
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sql_for_mdwiki.py
│   │   │   │   ├── sql_qids.py
│   │   │   │   └── sql_qids_others.py
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   └── sql_td_bot.py
│   │   │
│   │   ├── tools/
│   │   │   │
│   │   │   ├── models/
│   │   │   │
│   │   │   └── services/
│   │   │       │
│   │   │       ├── analytics/
│   │   │       │
│   │   │       ├── content/
│   │   │       │
│   │   │       ├── pages/
│   │   │       │
│   │   │       ├── reports/
│   │   │       │
│   │   │       ├── utils/
│   │   │       │
│   │   │       └── wikidata/
│   │   │
│   │   ├── __init__.py
│   │   └── to_sql_new.py
│   │
│   ├── md_core/
│   │   │
│   │   ├── mdpy/
│   │   │   │
│   │   │   ├── fixref/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fixref_text_new.py
│   │   │   │   ├── make_title_bot.py
│   │   │   │   └── start.py
│   │   │   │
│   │   │   ├── others/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── copy_qids.py
│   │   │   │   ├── export.py
│   │   │   │   ├── fixour.py
│   │   │   │   └── our.py
│   │   │   │
│   │   │   └── __init__.py
│   │   │
│   │   ├── p11143_bot/
│   │   │   ├── __init__.py
│   │   │   ├── bot.py
│   │   │   ├── filter_helps.py
│   │   │   └── wd_helps.py
│   │   │
│   │   ├── stats/
│   │   │   │
│   │   │   ├── editors/
│   │   │   │   ├── de.json
│   │   │   │   ├── es.json
│   │   │   │   ├── fr.json
│   │   │   │   ├── ja.json
│   │   │   │   ├── or.json
│   │   │   │   └── ru.json
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   ├── all2.py
│   │   │   ├── ar.py
│   │   │   ├── by_site.py
│   │   │   ├── editors.py
│   │   │   ├── qids.json
│   │   │   ├── qids.py
│   │   │   ├── sitelinks.py
│   │   │   └── start.sh
│   │   │
│   │   ├── unlinked_wb/
│   │   │   ├── __init__.py
│   │   │   ├── bot.py
│   │   │   └── hlps.py
│   │   │
│   │   ├── updates/
│   │   │   ├── __init__.py
│   │   │   ├── c2023.py
│   │   │   ├── date_after_20200701.txt
│   │   │   ├── date_before_20200701.txt
│   │   │   ├── io.py
│   │   │   └── listo.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── md_core_helps/
│   │   │
│   │   ├── apis/
│   │   │   │
│   │   │   ├── sup/
│   │   │   │   │
│   │   │   │   ├── cookies/
│   │   │   │   │   ├── wikidata_www_mr._ibrahem.txt
│   │   │   │   │   └── wikidata_www_mr.ibrahembot.txt
│   │   │   │   │
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cookies_bot.py
│   │   │   │   └── su_login.py
│   │   │   │
│   │   │   ├── wd_bots/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── wd_post_new.py
│   │   │   │   ├── wd_rest_new.py
│   │   │   │   └── wikidataapi_post.py
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   ├── all_pages.json
│   │   │   ├── cat_cach.py
│   │   │   ├── mdwiki_api_call.py
│   │   │   ├── mw_views.py
│   │   │   ├── user_accounts.py
│   │   │   ├── wiki_api.py
│   │   │   └── wikidataapi.py
│   │   │
│   │   ├── bots/
│   │   │   ├── __init__.py
│   │   │   ├── check_title.py
│   │   │   ├── en_to_md.py
│   │   │   └── py_tools.py
│   │   │
│   │   ├── __init__.py
│   │   └── tw.7z
│   │
│   ├── mdwiki_api/
│   │   ├── __init__.py
│   │   ├── mdwiki_page.py
│   │   └── wiki_page.py
│   │
│   ├── newapi/
│   │   │
│   │   ├── api_client/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── cookies_client.py
│   │   │   ├── exceptions.py
│   │   │   └── requests_handler.py
│   │   │
│   │   ├── client_wiki/
│   │   │   │
│   │   │   ├── api_utils/
│   │   │   │   │
│   │   │   │   ├── bot_edit/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── bot_edit_by_templates.py
│   │   │   │   │   ├── bot_edit_by_time.py
│   │   │   │   │   └── edit_checker.py
│   │   │   │   │
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ask_bot.py
│   │   │   │   ├── handel_errors.py
│   │   │   │   ├── txtlib.py
│   │   │   │   └── user_agent.py
│   │   │   │
│   │   │   ├── categories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── catdepth_new.py
│   │   │   │   └── category_db.py
│   │   │   │
│   │   │   ├── pages/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data.py
│   │   │   │   └── super_page.py
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   ├── all_apis.py
│   │   │   ├── bot_api.py
│   │   │   └── constants.py
│   │   │
│   │   ├── core/
│   │   │   └── exceptions.py
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── functions_timer.py
│   │   │   └── README.md
│   │   │
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── page.py
│   │
│   ├── td_core/
│   │   │
│   │   ├── after_translate/
│   │   │   │
│   │   │   ├── bots/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── add_to_mdwiki.py
│   │   │   │   ├── add_to_pages_users_db.py
│   │   │   │   ├── fixcat.py
│   │   │   │   ├── get_pages.py
│   │   │   │   └── users_pages.py
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   └── start_work.py
│   │   │
│   │   ├── db_work/
│   │   │   ├── __init__.py
│   │   │   ├── check_titles.py
│   │   │   ├── check_titles_helps.py
│   │   │   ├── days_7.py
│   │   │   └── get_red.py
│   │   │
│   │   ├── fix_user_pages/
│   │   │   ├── __init__.py
│   │   │   ├── bot.py
│   │   │   ├── del_records.py
│   │   │   ├── fix_it_db.py
│   │   │   ├── fix_it_db_new.py
│   │   │   └── user_bot.py
│   │   │
│   │   ├── mdcount/
│   │   │   │
│   │   │   ├── bots/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── countref_bots.py
│   │   │   │   ├── lead.py
│   │   │   │   ├── links.py
│   │   │   │   ├── ref.py
│   │   │   │   └── regex_scanner.py
│   │   │   │
│   │   │   └── __init__.py
│   │   │
│   │   ├── mdpages/
│   │   │   ├── __init__.py
│   │   │   ├── cashwd.py
│   │   │   ├── create_qids.py
│   │   │   ├── find_mt.py
│   │   │   ├── find_qids.py
│   │   │   └── findqids.sh
│   │   │
│   │   ├── td_other_qids/
│   │   │   ├── __init__.py
│   │   │   ├── all_pages.json
│   │   │   ├── fix_qids.py
│   │   │   ├── make_list.py
│   │   │   └── qids_help.py
│   │   │
│   │   ├── wd_works/
│   │   │   ├── __init__.py
│   │   │   └── recheck.py
│   │   │
│   │   ├── __init__.py
│   │   └── td_dirs.py
│   │
│   ├── titles_data/
│   │   ├── countrefs_and_words.py
│   │   ├── enwiki_views.py
│   │   ├── sqlviews_new.py
│   │   └── update_assessments.py
│   │
│   └── __init__.py
│
└── __init__.py

```