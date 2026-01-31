"""

python3 core8/pwb.py fix_use/mtab path:I:/mdwiki/mdwiki/public_html/td2/actions
python3 core8/pwb.py fix_use/mtab path:I:/mdwiki/mdwiki/public_html/td2/enwiki

"""

import json
import os
import re
import sys

tab = {
    "Infos\\TdConfig": ["Read_ini_file", "get_configs", "set_configs", "set_configs_all_file"],
    "TD": ["print_form_start1"],
    "Actions\\Functions": [
        "load_request",
        "escape_string",
        "strstartswithn",
        "strendswith",
        "test_print",
    ],
    "Actions\\WikiApi": ["get_url_result_curl", "make_view_by_number", "get_views"],
    "Actions\\MdwikiSql": [
        "execute_query",
        "sql_add_user",
        "update_settings",
        "insert_to_translate_type",
        "insert_to_projects",
        "get_all",
        "display_tables",
    ],
    "Actions\\MdwikiApi": ["get_url_params_result", "get_mdwiki_url_with_params"],
    "Actions\\Html": [
        "login_card",
        "makeCard",
        "makeColSm4",
        "makeDropdown",
        "make_cat_url",
        "make_col_sm_body",
        "make_datalist_options",
        "make_drop",
        "make_form_check_input",
        "make_input_group",
        "make_input_group_no_col",
        "make_mail_icon",
        "make_mdwiki_title",
        "make_mdwiki_user_url",
        "make_modal_fade",
        "make_project_to_user",
        "make_talk_url",
        "make_target_url",
        "make_translation_url",
    ],
    "Actions\\HtmlSide": ["create_side"],
    "EnWiki\\Fixes\\DelMtRefs": ["del_empty_refs"],
    "EnWiki\\Fixes\\ExpendRefs": ["refs_expend_work"],
    "EnWiki\\Fixes\\FixCats": ["remove_categories"],
    "EnWiki\\Fixes\\FixImages": ["remove_images"],
    "EnWiki\\Fixes\\fix_langs_links": ["remove_lang_links"],
    "EnWiki\\Fixes\\FixTemps": ["remove_templates"],
    "EnWiki\\Fixes\\RefWork": ["check_one_cite", "remove_bad_refs"],
    "EnWiki\\API": [
        "getLoginToken",
        "loginRequest",
        "getCSRFToken",
        "send_params",
        "do_edit",
        "Find_pages_exists_or_not",
    ],
    "EnWiki\\FixText": ["text_changes_work"],
    "EnWiki\\Start": ["startTranslatePhp", "TranslatePhpEditText"],
    "WikiParse\\Category": ["get_categories"],
    "WikiParse\\Citations": ["get_name", "getCitations", "get_full_refs", "getShortCitations"],
    "WikiParse\\Template": ["getTemplate"],
    "Leaderboard\\Camps": ["camps_list"],
    "Leaderboard\\Graph": ["graph_html", "print_graph_from_sql", "print_graph_for_table", "print_graph_tab"],
    "Leaderboard\\Index": ["print_cat_table"],
    "Leaderboard\\Langs": ["make_filter_form"],
    "Leaderboard\\LeaderTables": ["makeSqlQuery", "createNumbersTable", "makeUsersTable", "makeLangTable"],
    "Leaderboard\\LeadHelp": ["make_td_fo_user", "make_table_lead"],
    "Leaderboard\\Users": ["make_filter_form"],
    "Results\\GetCats": [
        "start_with",
        "get_in_process",
        "open_json_file",
        "get_cat_from_cache",
        "get_categorymembers",
        "get_mmbrs",
        "get_mdwiki_cat_members",
        "get_cat_exists_and_missing",
    ],
    "Results\\GetResults": ["get_results"],
    "Results\\ResultsTable": ["sort_py_PageViews", "sort_py_importance", "make_one_row", "make_results_table"],
}


def make_find_rep():
    # ---
    new = {}
    # ---
    for file, functions in tab.items():
        # ---
        for func in functions:
            # ---
            r"use function Actions\HtmlSide\create_side;",
            line = f"use function {file}\\{func};"
            # ---
            new[func] = line
    # ---
    return new


def one_file(file):
    # ---
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # ---
    print(f"\n\n_______{file=}, {len(lines)=}")
    # ---
    ns = None
    ta = []
    # ---
    for line in lines:
        # ---
        if line.startswith(" ") or line.startswith("\t") or line.startswith("//") or not line.strip():
            continue
        # ---
        if not line.startswith("namespace ") and not line.startswith("function "):
            continue
        # ---
        line = line.strip()
        # ---
        print([line])
        # ---
        # match page namespace like:
        # namespace EnWiki\API;
        # ---
        ma = re.match(r"^namespace (.*?)\;$", line)
        if ma:
            ns = ma.group(1)
            continue
        # ---
        # match page function like:
        # function getLoginToken($session)
        # ---
        ma = re.match(r"^function (.*?)\s*\(", line)
        if ma:
            ta.append(ma.group(1))
    # ---
    return ns, ta


def start():
    path = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg == "path":
            path = value.strip()
    # ---
    print(f" <<blue>> work on path : {path}\n" * 3)
    # ---
    if not os.path.exists(path):
        print(" <<blue>> path not exist")
        return
    # ---
    from fix_use.add import add_use

    # ---
    tab2 = {}
    # ---
    for root, dirs, files in os.walk(path, topdown=True):
        # ---
        for file in files:
            # ---
            if not file.endswith(".php"):
                continue
            # ---
            file_path = os.path.join(root, file)
            # ---
            ns, ta = one_file(file_path)
            # ---
            if not ns or not ta:
                continue
            # ---
            if ns in tab:  # and ta == tab[ns]:
                continue
            # ---
            tab2[ns] = ta
            # ---
            ta2 = [f"use function {ns}\\{func};" for func in ta]
            # ---
            add_use(file_path, ns_line=f"namespace {ns};", add_lines=ta2)
            # ---
            if "break" in sys.argv:
                break
    # ---
    print(json.dumps(tab2, indent=4))


if __name__ == "__main__":
    # ---
    start()
