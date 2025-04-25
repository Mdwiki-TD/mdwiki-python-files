#!/usr/bin/python3
"""
from fix_user_pages.user_bot import get_new_user
"""
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from db_work.check_titles_helps import WikiPage, users_infos

db_users = sql_for_mdwiki.get_db_users()


def count_users(revisions):
    tab = {}
    # ---
    for x in revisions:
        user = x.get("user")
        # ---
        tab.setdefault(user, 0)
        # ---
        tab[user] += 1
    # ---
    # sort tab
    tab = dict(sorted(tab.items(), key=lambda x: x[1], reverse=True))
    # ---
    return tab


def filter_revisions(lang, revisions):
    # ---
    infos = users_infos(lang, [x.get("user") for x in revisions if x.get("user")])
    # ---
    infos = {x["name"]: x for x in infos}
    # ---
    for x in revisions[:]:
        x_user = x.get("user", "")
        # ---
        user_data = infos.get(x_user, {})
        # ---
        if user_data.get("invalid") or user_data.get("missing"):
            revisions.remove(x)
            continue
        # ---
        groups = user_data.get("groups", [])
        # ---
        if "bot" in groups or "temp" in groups:
            revisions.remove(x)
            continue
        # ---
        if x_user.lower().endswith("bot"):
            # ---
            revisions.remove(x)
            continue
        # ---
    # ---
    return revisions


def get_new_user(new_target, lang, user):
    # ---
    page = WikiPage(new_target, lang, family="wikipedia")
    # ---
    # user = page.get_user()
    # userinfo    = page.get_userinfo() # "id", "name", "groups"
    revisions = page.get_revisions(rvprops=[])
    # ---
    revisions = filter_revisions(lang, revisions)
    # ---
    if not revisions:
        return ""
    # ---
    second_revid = 0
    # ---
    for x in revisions:
        x_user = x.get("user")
        if "parentid" in x and x["parentid"] == 0:
            # ---
            second_revid = x["revid"]
            # ---
            if x_user != user:
                printe.output(f"<<red>> user:{user} new page not new!, created by :{x_user}")
                return False
            else:
                printe.output(f"<<green>> new page created by :{x_user}")
            # ---
            break
    # ---
    false_users = ["Annacecilia2", "Doc James"]
    # ---
    if user in false_users:
        # ---
        revs = [x for x in revisions if x["parentid"] == second_revid]
        # ---
        if revs and revs[0]["user"] not in false_users:
            # ---
            rev_user = revs[0]["user"]
            # ---
            in_db = rev_user in db_users
            # ---
            printe.output(f"<<green>> rev_user is :{rev_user}, {in_db=}")
            # ---
            if in_db:
                return rev_user
        # ---
        user_2nd = ""
        # ---
        users_count = count_users(revisions)
        # ---
        for x in revisions:
            # ---
            x_user = x.get("user")
            # ---
            x_count = users_count.get(x_user, 0)
            # ---
            if x_user not in false_users:
                # ---
                if not user_2nd:
                    user_2nd = x_user
                # ---
                in_db = x_user in db_users
                # ---
                printe.output(f"<<green>> x_user is: {x_user}, {in_db=}, {x_count=}")
                # ---
                if not in_db and x_count == 1:
                    continue
                # ---
                return x_user
        # ---
        return user_2nd
    # ---
    # print(f"get_new_user: {user=}, {revisions=}")
    # ---
    return ""
