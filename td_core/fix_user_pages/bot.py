#!/usr/bin/python3
"""

مراجعة المقالات المنشورة في نطاق المستخدم
والتحقق اذا تم نقلها الى النطاق الرئيسي يتم الآتي:
1. ربطها بويكي بيانات
2. تحديث بيانات الترجمة في قاعدة البيانات

python3 core8/pwb.py fix_user_pages/bot test -lang:ar
python3 core8/pwb.py fix_user_pages/bot test

"""
import sys
import tqdm
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from db_work.check_titles_helps import get_new_target_log, Find_pages_exists, WikiPage
# from fix_user_pages.fix_it_db import work_in_new_tabs_to_db
from fix_user_pages.fix_it_db_new import work_in_new_tabs_to_db_new
from fix_user_pages.user_bot import get_new_user

skip_by_lang = {
    "ar": ["الأنسولين"],
}
db_users = sql_for_mdwiki.get_db_users()

deleted_pages = []
new_tabs_to_db = []
qids_all = {}
to_set = {}
text = []

already_in_db = sql_for_mdwiki.get_all_from_table(table_name="pages_users_to_main")
already_in_db = [x["id"] for x in already_in_db]


def get_titles(lang=""):
    # ---
    if "test" in sys.argv and not lang:
        return {"ar": [
            { "id": 5, "title": "Beta blocker toxicity", "word": 0, "translate_type": 0, "cat": 0, "lang": "ar", "user": "Mina karaca", "target": "user:Mina karaca/التسمم بحاصرات بيتا", "date": 0, "pupdate": "2024-02-11", "add_date": "2024-02-15 03:00:00", "deleted": 0 }
        ]}
    # ---
    pages_users = sql_for_mdwiki.get_all_pages_all_keys(lang=lang, table="pages_users")
    pages_users_tab = {}
    # ---
    for tab in pages_users:
        # ---
        if tab["id"] in already_in_db:
            continue
        # ---
        lang = tab["lang"]
        # ---
        pages_users_tab.setdefault(lang, [])
        # ---
        pages_users_tab[lang].append(tab)
    # ---
    return pages_users_tab


def work_one_tab(tab, missing, redirects):
    # ---
    print("---------------- work_one_tab -----------------------")
    # ---
    iid, lang, target = tab["id"], tab["lang"], tab["target"]
    # ---
    skip_it = skip_by_lang.get(lang, {})
    # ---
    if target in skip_it:
        printe.output(f"<<yellow>> skip {target}")
        return {}
    # ---
    new_target = ""
    # ---
    if target in missing:
        printe.output(f'<<red>> page "{target}" not exists in {lang}')
        deleted, new_target = get_new_target_log(lang, target)
        if deleted:
            printe.output(f'<<red>> page "{target}" deleted in {lang}')
            deleted_pages.append(iid)
        # ---
    elif target in redirects:
        page = WikiPage(target, lang, family="wikipedia")
        new_target = page.get_redirect_target()
    # ---
    if new_target:
        printe.output(f"<<yellow>> work_one_tab: {target=}, {new_target=}")
        # ---
        page2 = WikiPage(new_target, lang, family="wikipedia")
        # ---
        if page2.exists():
            ns = page2.namespace() or page2.ns
            # ---
            qids_all.setdefault(lang, {})
            qids_all[lang][new_target] = page2.get_qid()
            # ---
            tab["qid"] = page2.get_qid()
            # ---
            printe.output(f"<<yellow>> new_target exists, ns: {ns}")
            # ---
            if not page2.isRedirect() and ns == 0 :
                # ---
                to_set[new_target] = tab
                # sql_for_mdwiki.set_target_where_id(new_target, iid)
                # ---
                text.append([lang, target, new_target])
                # ---
                return {new_target : tab}
        # else:
        #     printe.output(f'<<red>> page "{new_target}" deleted from {lang}')
        #     deleted.append(iid)
    # ---
    return {}


def work_in_titles(lang, tabs):
    # ---
    qids_all.setdefault(lang, {})
    # ---
    printe.output(f"<<green>> lang:{lang}, has {len(tabs)} pages")
    # ---
    titles = [x["target"] for x in tabs]
    # ---
    pages = Find_pages_exists(lang, titles)
    # ---
    missing = [x for x, v in pages.items() if not v]
    redirects = [x for x, v in pages.items() if v == "redirect"]
    # ---
    printe.output(f"lang:{lang}, missing:{len(missing)}, redirects:{len(redirects)}")
    # ---
    new_tabs = [tab for tab in tabs if tab["target"] in missing or tab["target"] in redirects]
    # ---
    if len(titles) != len(new_tabs):
        printe.output(f"lang:{lang}, has {len(new_tabs)} new tabs")
    # ---
    to_set_new = {}
    # ---
    for tab in tqdm.tqdm(new_tabs):
        tat = work_one_tab(tab, missing, redirects)
        to_set_new.update(tat)
    # ---
    toto = []
    # ---
    for new_target, tab in to_set_new.items():
        xx = work_in_to_set(new_target, tab)
        if xx:
            toto.append(xx)
    # ---
    # work_in_new_tabs_to_db(new_tabs_to_db)
    # ---
    work_in_new_tabs_to_db_new(toto)


def work_in_to_set(new_target, tab):
    # ---
    print("------------- work_in_to_set ---------------")
    # ---
    # {'id': '3381', 'title': 'Sympathetic crashing acute pulmonary edema', 'lang': 'ar', 'user': 'Annacecilia2', 'pupdate': '2025-03-26', 'target': 'User:Annacecilia2/Sympathetic crashing acute pulmonary edema', 'add_date': '2025-03-26 23:43:12'}
    # ---
    tab_id = tab['id']
    # ---
    new_tab = tab.copy()
    new_tab["target"] = new_target
    # ---
    printe.output(f"<<green>> work_in_to_set() new_target:{new_target}")
    # ---
    user = new_tab["user"]
    # ---
    newuser = get_new_user(new_target, new_tab["lang"], user)
    # ---
    if not newuser:
        return {}
    # ---
    new_tab["user"] = newuser
    # new_tab["qid"] = qids_all.get(new_tab["lang"], {}).get(new_target)
    # ---
    printe.output(f"<<purple>> {user=}, {newuser=}")
    # ---
    new_tabs_to_db.append({"old": tab, "new": new_tab})
    # ---
    # if "test" not in sys.argv: sql_for_mdwiki.set_target_where_id(new_target, tab_id)
    # ---
    return {"old": tab, "new": new_tab}


def start():
    # ---
    lang = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "-lang":
            lang = value
    # ---
    titles_by_lang = get_titles(lang=lang)
    # ---
    printe.output(f"<<green>> len of titles_by_lang {len(titles_by_lang)}")
    # ---
    for lang, tabs in titles_by_lang.items():
        # ---
        work_in_titles(lang, tabs)
    # ---
    '''
    printe.output(f"len of to_set {len(to_set)}")
    # ---
    for new_target, tab in to_set.items():
        work_in_to_set(new_target, tab)
    # ---
    # work_in_new_tabs_to_db(new_tabs_to_db)
    # ---
    work_in_new_tabs_to_db_new(new_tabs_to_db)'''


if __name__ == "__main__":
    start()
