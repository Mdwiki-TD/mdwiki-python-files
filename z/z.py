"""

python3 core8/pwb.py z/z


English Term;Dzongkha Term;Dzongkha Explanation
abalienation;འཆོལ་ལྫོ་སྫོ་ལྫོ།;སེམས་ཏན་ཏན་མེད་འགྱོ་བ།
abarticulation;ཚིགས་དཀྲུག་པ།;རྐངམ་དང་ལག་པའི་ཚིགས་དཀྲུག་ི།


# read dictionary(oc_resolved).csv extract English Term;Dzongkha Term;Dzongkha Explanation to english_terms

"""

import sys
import json
import Levenshtein
# from newapi.page import NEW_API
from tqdm import tqdm
from newapi.page import MainPage
# from newapi.wd_sparql import get_query_result
from pathlib import Path

from newapi.api_utils import wd_sparql
import api_wd_z

Dir = Path(__file__).parent

# api = NEW_API('en', family='wikipedia')
# api.Login_to_wiki()

qids_file_multi = Dir / "jsons/qids_multi.json"
qids_file_mt = Dir / "jsons/qids_empty.json"
qids_file = Dir / "jsons/qids.json"
data_file = Dir / "jsons/data.json"

results = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}

to_add = json.loads(data_file.read_text('utf-8')) if data_file.exists() else []

data_ready_file = Dir / "jsons/data_ready.json"
data_ready = json.loads(data_ready_file.read_text('utf-8'))

if "fix_data_ready" in sys.argv:
    data_ready = {x.lower(): v for x, v in data_ready.items()}
    # ---
    with open(data_ready_file, 'w', encoding='utf-8') as file:
        json.dump(data_ready, file, ensure_ascii=False, indent=4)

langs_results = {}


def dump_one(file, data):
    # ---
    print(f"Dump : {len(data)} to: {file.name}")
    # ---
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if "clear" in sys.argv:
    # clear results with multi qids
    # ---
    results = {
        k: [] if len(v) > 1 else v
        for k, v in results.items()
    }
    # ---
    dump_one(qids_file, results)
    dump_one(qids_file_multi, {})
    # ---
    exit()


def dump_data():
    results_x = {z : list(set(v)) for z, v in results.items()}
    # ---
    dump_one(qids_file, results_x)
    # ---
    results_x_multi = {z : v for z, v in results_x.items() if len(v) > 1}
    # ---
    dump_one(qids_file_multi, results_x_multi)
    # ---
    results_x_empty = {z : v for z, v in results_x.items() if len(v) == 0 or not v}
    # ---
    dump_one(qids_file_mt, results_x_empty)
    # ---
    dump_one(data_ready_file, data_ready)


def get_qids(english_terms_new):

    for term in tqdm(english_terms_new, desc="Processing terms"):
        results.setdefault(term, [])
        page = MainPage(term, 'en', family='wikipedia')
        if page.exists():
            qid = page.get_qid()  # يحصل على معرف Wikidata
            if qid:
                print(f"{term}: {qid}")
                results[term].append(qid)

    dump_data()


def get_english_terms():

    english_terms = to_add.keys()

    print(f"len of english_terms: {len(english_terms)}")

    english_terms_new = [x for x in english_terms if not results.get(x.strip(), [])]
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
    # ---
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
    return qid_main, best_label, highest_score


def search_wd(english_terms_new):
    # results = wd_sparql.get_query_result(query)
    for term in tqdm(english_terms_new, desc="Processing terms"):
        # ---
        results.setdefault(term, [])
        # ---
        qid, best_label, highest_score = get_term_qid(term)
        # ---
        print(f"{term}: {qid} {best_label} {highest_score}")
        # ---
        if qid:
            results[term].append(qid)
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
    english_terms_new = get_english_terms()
    # ---
    # get_qids(english_terms_new)
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
