"""

python3 core8/pwb.py z/find_qids


English Term;label;description
abalienation;འཆོལ་ལྫོ་སྫོ་ལྫོ།;སེམས་ཏན་ཏན་མེད་འགྱོ་བ།
abarticulation;ཚིགས་དཀྲུག་པ།;རྐངམ་དང་ལག་པའི་ཚིགས་དཀྲུག་ི།


# read dictionary(oc_resolved).csv extract English Term;label;description to english_terms

"""

import sys
import json
import Levenshtein
from tqdm import tqdm
from newapi import printe
# from newapi.wd_sparql import get_query_result
from pathlib import Path

from newapi.page import NEW_API, MainPage
api_new = NEW_API('en', family='wikipedia')

from newapi.api_utils import wd_sparql
from api_z import api_wd_z

JsonsDir = Path(__file__).parent / "jsons"

qids_file_multi = JsonsDir / "qids_multi.json"
qids_file_mt = JsonsDir / "qids_empty.json"
qids_file = JsonsDir / "qids.json"
data_file = JsonsDir / "data.json"

results = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}
to_add = json.loads(data_file.read_text('utf-8')) if data_file.exists() else []

old_length = {
    "qids.json": len(results),
    "data.json": len(to_add),
    "qids_empty.json": 0,
    "qids_multi.json": 0,
}

langs_results = {}


def dump_one(file, data):
    # ---
    old_len = old_length.get(file.name) or len(json.loads(file.read_text('utf-8')))
    # ---
    print(f"Dump : {len(data):,} old_len: {old_len:,} to: {file.name}")
    # ---
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if "fix_qids" in sys.argv:
    # ---
    results = {
        k: {qid: {"score" : 1, "matched_label" : "", } for qid in v}
        for k, v in results.items()
    }
    # ---
    dump_one(qids_file, results)
    dump_one(qids_file_multi, {})
    # ---
    exit()


def dump_data():
    results_x = {z : v for z, v in results.items()}
    # ---
    dump_one(qids_file, results_x)
    # ---
    resultsx_multi = {z : v for z, v in results_x.items() if len(v) > 1}
    # ---
    dump_one(qids_file_multi, resultsx_multi)
    # ---
    resultsx_empty = {z : v for z, v in results_x.items() if len(v) == 0 or not v}
    # ---
    dump_one(qids_file_mt, resultsx_empty)


def get_qids(english_terms_new):
    # ---
    for term in tqdm(english_terms_new, desc="Processing terms"):
        results.setdefault(term, {})
        page = MainPage(term, 'en', family='wikipedia')
        if page.exists():
            qid = page.get_qid()  # يحصل على معرف Wikidata
            if qid:
                printe.output(f"<<yellow>> {term}: {qid}")
                results[term][qid] = {
                    "score" : 2,
                    "matched_label" : term,
                }
    # ---
    dump_data()


def get_qids_new(english_terms_new):
    # ---
    titles = list(english_terms_new)
    # ---
    pages = api_new.Find_pages_exists_or_not_with_qids(english_terms_new, get_redirect=True, use_user_input_title=True)
    # ---
    with open(JsonsDir / "pages.json", 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=4)
    # ---
    exists = {x: d for x, d in pages.items() if d.get("exist")}
    # ---
    not_exists = [x.lower() for x, z in pages.items() if not z.get("exist")]
    # ---
    print(f"all:{len(english_terms_new)} \t exists: {len(exists)} \t not_exists: {len(not_exists)}")
    # ---
    for term in tqdm(english_terms_new, desc="Processing terms"):
        # ---
        results.setdefault(term, {})
        # ---
        data = exists.get(term) or {}
        # ---
        qid = data.get("wikibase_item")
        # ---
        if qid:
            printe.output(f"<<yellow>> {term}: {qid}")
            results[term][qid] = {
                "score" : 2,
                "matched_label" : term,
            }
    # ---
    dump_data()


def get_english_terms():

    english_terms = to_add.keys()

    print(f"len of english_terms: {len(english_terms)}")

    english_terms_new = [x for x in english_terms if not results.get(x.strip(), {})]
    # ---
    print(f"len of english_terms_new: {len(english_terms_new)}")
    # ---
    return english_terms_new


def sparql_work(english_terms_new):
    # استعلام SPARQL للبحث عن العناصر بالتسميات الإنجليزية
    query = """
        SELECT ?item ?itemLabel WHERE {

        ?item rdfs:label ?label.
        FILTER(CONTAINS(LCASE(?label), "abdomen") && LANG(?label) = "en")
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 10
    """
    resultsx = wd_sparql.get_query_result(query)


def get_term_qid(term):
    # ---
    json1 = api_wd_z.wbsearchentities(term, "en", match_alias=True) or {}
    # ---
    # print(f"term: {term}")
    # print(json1)
    # ---
    # {'Q56690849': {'label': 'abaliénation s. f.', 'lang': 'fr'}, 'Q305266': {'label': 'Abalienation', 'lang': 'en'}}
    # ---
    qid_main = ""
    best_label = None
    highest_score = 0.0
    # ---
    for qid, data in json1.items():
        # ---
        label = data.get("label")
        lang = data.get("lang")
        # ---
        if lang != "en" and lang != "mul" and "alllangs" not in sys.argv:
            langs_results.setdefault(lang, 0)
            langs_results[lang] += 1
            continue
        # ---
        score = Levenshtein.ratio(term, label)
        # ---
        if score > highest_score:
            highest_score = score
            best_label = label
            qid_main = qid
        # ---
        # if label.lower() != term.lower(): continue
        # ---
        # print(f"{label}: {lang} {qid}")
        # ---
        # qid_main = qid
        # ---
        # break
    # ---
    highest_score = round(highest_score, 3)
    # ---
    return qid_main, best_label, highest_score


def search_wd(english_terms_new):
    # results = wd_sparql.get_query_result(query)
    for term in tqdm(english_terms_new, desc="Processing terms"):
        # ---
        results.setdefault(term, {})
        # ---
        qid, best_label, highest_score = get_term_qid(term)
        # ---
        print(f"{term}: {qid} {best_label} {highest_score}")
        # ---
        if qid and highest_score > 0:
            results[term][qid] = {
                "score" : highest_score,
                "matched_label" : best_label  # .replace('"', "'"),
            }
        # ---
        if "break" in sys.argv:
            break
    # ---
    dump_data()


def start():
    # ---
    # for term in english_terms:
    #     search_results = api.Search(value=term, ns="0", srlimit="5")
    #     results[term] = search_results

    # ---
    if "work_all" in sys.argv:
        get_qids_new(to_add.keys())
        return
    # ---
    english_terms_new = get_english_terms()
    # ---
    search_wd(english_terms_new)
    # ---


def print_langs_results():
    print(f"langs_results: {len(langs_results)}")
    # ---
    if langs_results:
        # ---
        for lang, count in langs_results.items():
            print(f"{lang}: {count}")
        # ---
        print("add 'alllangs' to sys.argv to use all langs\n" * 3)


def test():
    term = "costae"
    # ---
    result = get_term_qid(term)
    # ---
    print(f"result: ({result})")


if __name__ == '__main__':
    if "test" in sys.argv:
        test()
    else:
        start()
    # ---
    print_langs_results()
