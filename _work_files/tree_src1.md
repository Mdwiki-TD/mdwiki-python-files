```
src1/
│
├── copy_text/
│   ├── __init__.py
│   ├── bot.py
│   ├── files_list.py
│   ├── html_bot.py
│   ├── README.md
│   ├── scan_files.py
│   └── text_bot.py
│
├── copy_to_en/
│   │
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── alltext_changes.py
│   │   ├── fix_refs_names.py
│   │   ├── ref.py
│   │   ├── ref2.py
│   │   └── text_changes.py
│   │
│   ├── __init__.py
│   ├── all_pages.json
│   ├── bot.py
│   ├── mdwikicx.py
│   ├── medwiki.py
│   ├── revid.py
│   ├── tf_page.py
│   └── x.py
│
├── find_replace_bot/
│   ├── __init__.py
│   ├── bot.py
│   ├── one_job.py
│   └── README.md
│
├── fix_cs1/
│   │
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── find_journal.py
│   │   ├── pmid.py
│   │   └── temps_list.py
│   │
│   ├── fix_cs_params/
│   │   ├── __init__.py
│   │   └── bot.py
│   │
│   ├── __init__.py
│   ├── archive_date_maker.py
│   ├── bot.py
│   └── fix_p.py
│
├── fix_use/
│   ├── __init__.py
│   ├── add.py
│   ├── bot.py
│   ├── mtab.py
│   └── write_bot.py
│
├── md_core/
│   │
│   ├── add_rtt/
│   │   │
│   │   ├── r_column_bots/
│   │   │   ├── __init__.py
│   │   │   ├── add_r_column.py
│   │   │   └── pup_table.py
│   │   │
│   │   ├── __init__.py
│   │   ├── add_r_col_to_file.py
│   │   ├── bot.py
│   │   ├── page_text.txt
│   │   ├── pup.py
│   │   └── remove.py
│   │
│   ├── commons_svg/
│   │   ├── bot.py
│   │   ├── list.py
│   │   ├── list.wiki
│   │   └── svg_languages.json
│   │
│   ├── mdpy/
│   │   ├── fix_duplicate.py
│   │   ├── fixred.py
│   │   ├── imp.py
│   │   ├── mdjobs.sh
│   │   ├── orred.py
│   │   ├── red.py
│   │   └── replace1.py
│   │
│   └── updates/
│       └── medicine_articles.py
│
├── md_core_helps/
│   │
│   └── one_time/
│       │
│       ├── niosh/
│       │   │
│       │   ├── by_title/
│       │   │   ├── 1-1.json
│       │   │   ├── 1-2.json
│       │   │   ├── 2-1.json
│       │   │   ├── 2-2.json
│       │   │   ├── 3-1.json
│       │   │   ├── 3-2.json
│       │   │   ├── 4-1.json
│       │   │   ├── 4-2.json
│       │   │   ├── 5-1.json
│       │   │   ├── 5-2.json
│       │   │   ├── 6.json
│       │   │   └── all.json
│       │   │
│       │   ├── by_url/
│       │   │   ├── 1-1.json
│       │   │   ├── 1-2.json
│       │   │   ├── 2-1.json
│       │   │   ├── 2-2.json
│       │   │   ├── 3-1.json
│       │   │   ├── 3-2.json
│       │   │   ├── 4-1.json
│       │   │   ├── 4-2.json
│       │   │   ├── 5-1.json
│       │   │   ├── 5-2.json
│       │   │   ├── 6.json
│       │   │   └── all.json
│       │   │
│       │   ├── downloads/
│       │   │   ├── 1-1.txt
│       │   │   ├── 1-2.txt
│       │   │   ├── 2-1.txt
│       │   │   ├── 2-2.txt
│       │   │   ├── 3-1.txt
│       │   │   ├── 3-2.txt
│       │   │   ├── 4-1.txt
│       │   │   ├── 4-2.txt
│       │   │   ├── 5-1.txt
│       │   │   ├── 5-2.txt
│       │   │   └── 6.txt
│       │   │
│       │   ├── downloads_js/
│       │   │   ├── 1-1.txt.json
│       │   │   ├── 1-2.txt.json
│       │   │   ├── 2-1.txt.json
│       │   │   ├── 2-2.txt.json
│       │   │   ├── 3-1.txt.json
│       │   │   ├── 3-2.txt.json
│       │   │   ├── 4-1.txt.json
│       │   │   ├── 4-2.txt.json
│       │   │   ├── 5-1.txt.json
│       │   │   ├── 5-2.txt.json
│       │   │   ├── 6.txt.json
│       │   │   └── cite_all_links.json
│       │   │
│       │   ├── find/
│       │   │   ├── __init__.py
│       │   │   ├── both.py
│       │   │   ├── qu.py
│       │   │   └── search.py
│       │   │
│       │   ├── jsons/
│       │   │   ├── all_links.json
│       │   │   ├── both.json
│       │   │   └── extlinks.json
│       │   │
│       │   ├── __init__.py
│       │   ├── bot.py
│       │   ├── get.py
│       │   └── s.py
│       │
│       ├── prior/
│       │   │
│       │   ├── bots/
│       │   │   ├── __init__.py
│       │   │   ├── readjsons.py
│       │   │   └── remove_wikis.py
│       │   │
│       │   ├── json_en/
│       │   │   ├── __init__.py
│       │   │   ├── en_1.json
│       │   │   ├── en_10.json
│       │   │   ├── en_11.json
│       │   │   ├── en_12.json
│       │   │   ├── en_13.json
│       │   │   ├── en_14.json
│       │   │   ├── en_15.json
│       │   │   ├── en_2.json
│       │   │   ├── en_3.json
│       │   │   ├── en_4.json
│       │   │   ├── en_5.json
│       │   │   ├── en_6.json
│       │   │   ├── en_7.json
│       │   │   ├── en_8.json
│       │   │   ├── en_9.json
│       │   │   └── lists.py
│       │   │
│       │   ├── json_langs/
│       │   │   ├── 1.json
│       │   │   ├── 10.json
│       │   │   ├── 11.json
│       │   │   ├── 12.json
│       │   │   ├── 13.json
│       │   │   ├── 14.json
│       │   │   ├── 15.json
│       │   │   ├── 2.json
│       │   │   ├── 3.json
│       │   │   ├── 4.json
│       │   │   ├── 5.json
│       │   │   ├── 6.json
│       │   │   ├── 7.json
│       │   │   ├── 8.json
│       │   │   ├── 9.json
│       │   │   ├── __init__.py
│       │   │   └── lists.py
│       │   │
│       │   ├── log/
│       │   │   ├── Anatomy and others.txt
│       │   │   ├── Brain, mind, endo, and senses.txt
│       │   │   ├── Dentistry.txt
│       │   │   ├── Emergency medicine.txt
│       │   │   ├── en.txt
│       │   │   ├── Engineering.txt
│       │   │   ├── Essential meds.txt
│       │   │   ├── NTD and other ID.txt
│       │   │   ├── OBGYN-Peds.txt
│       │   │   ├── Other drugs - procedures.txt
│       │   │   └── Tumors.txt
│       │   │
│       │   ├── __init__.py
│       │   ├── add_old.py
│       │   ├── all_pages_states.json
│       │   ├── get_them.py
│       │   ├── log_test.txt
│       │   ├── p4.py
│       │   ├── read5.py
│       │   └── text_bot.py
│       │
│       ├── priorviews/
│       │   │
│       │   ├── bots/
│       │   │   ├── __init__.py
│       │   │   ├── count_words.py
│       │   │   ├── get_translator.py
│       │   │   ├── gt_blame.py
│       │   │   ├── helps.py
│       │   │   ├── sections_links.py
│       │   │   ├── sections_text.py
│       │   │   └── w_all.py
│       │   │
│       │   ├── find/
│       │   │   ├── __init__.py
│       │   │   ├── find_blame.py
│       │   │   ├── find_creator.py
│       │   │   ├── find_translators.py
│       │   │   ├── find_views.py
│       │   │   └── find_word.py
│       │   │
│       │   ├── lists/
│       │   │   ├── __init__.py
│       │   │   ├── all_pages_states.json
│       │   │   ├── blames.json
│       │   │   ├── blames.json_1
│       │   │   ├── count_views_by_lang.json
│       │   │   ├── creators.py
│       │   │   ├── creators_as_translators.json
│       │   │   ├── creators_by_lang.json
│       │   │   ├── creators_to_translators.py
│       │   │   ├── links_by_section.py
│       │   │   ├── secs_links.json
│       │   │   ├── tab_new.json
│       │   │   ├── translators.py
│       │   │   ├── views.py
│       │   │   ├── views_mdwiki_langs.json
│       │   │   ├── views_mdwiki_langs1.json
│       │   │   ├── words.py
│       │   │   ├── words_mdwiki_langs.json
│       │   │   └── ‏translators_mdwiki_langs -1.json
│       │   │
│       │   ├── __init__.py
│       │   ├── add_blame_to_tra.py
│       │   ├── bot.py
│       │   ├── by_lang.py
│       │   ├── co.py
│       │   ├── langs.py
│       │   ├── sea55.json
│       │   └── start.sh
│       │
│       ├── WHOem/
│       │   │
│       │   ├── lists/
│       │   │   ├── lang_links.json
│       │   │   ├── lang_links_mdtitles.json
│       │   │   ├── links_not_found.json
│       │   │   ├── md_links.json
│       │   │   └── views.json
│       │   │
│       │   ├── __init__.py
│       │   ├── bot.py
│       │   ├── find_views_by_lang.py
│       │   ├── make_text.py
│       │   └── start.sh
│       │
│       ├── wikiblame/
│       │   ├── __init__.py
│       │   ├── bot.py
│       │   └── bot1.py
│       │
│       └── __init__.py
│
├── named_param/
│   ├── __init__.py
│   └── named_param.py
│
├── newupdater/
│   │
│   ├── new_updater/
│   │   │
│   │   ├── bots/
│   │   │   ├── __init__.py
│   │   │   ├── expend.py
│   │   │   ├── expend_new.py
│   │   │   ├── old_params.py
│   │   │   └── Remove.py
│   │   │
│   │   ├── lists/
│   │   │   ├── __init__.py
│   │   │   ├── bot_params.py
│   │   │   ├── chem_params.py
│   │   │   ├── expend_lists.py
│   │   │   └── identifier_params.py
│   │   │
│   │   ├── __init__.py
│   │   ├── chembox.py
│   │   ├── drugbox.py
│   │   ├── helps.py
│   │   ├── MedWorkNew.py
│   │   ├── mv_section.py
│   │   └── resources_new.py
│   │
│   ├── __init__.py
│   ├── mdapi.py
│   ├── med.py
│   ├── medask.py
│   ├── README.md
│   └── tests.7z
│
├── td_core/
│   │
│   └── coby_data/
│       │
│       ├── by_qid/
│       │
│       ├── by_title/
│       │   ├── __init__.py
│       │   └── all_articles.py
│       │
│       ├── __init__.py
│       ├── copy_assessments.py
│       ├── copy_enwiki_pageviews.py
│       ├── copy_refs_2.py
│       ├── copy_word_2.py
│       ├── copy_word_table.py
│       ├── enwiki_pageviews.txt
│       └── sitelinks.py
│
├── wprefs/
│   │
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── duplicate.py
│   │   ├── es_months.py
│   │   ├── es_mv.txt
│   │   ├── es_mv_fixed.txt
│   │   ├── es_refs.py
│   │   ├── es_section.py
│   │   ├── fix_pt_months.py
│   │   └── test_pt_months.py
│   │
│   ├── __init__.py
│   ├── bot.py
│   ├── bot1.py
│   ├── es.py
│   ├── files.py
│   ├── helps.py
│   ├── infobox.py
│   ├── README.MD
│   ├── reffixed.csv
│   ├── wpref_text.py
│   └── wprefs_api.py
│
├── old scripts.rar
├── te.rar
└── update_med_views.zip

```