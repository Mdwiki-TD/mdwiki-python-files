"""

python3 core8/pwb.py z


English Term;Dzongkha Term;Dzongkha Explanation
abalienation;འཆོལ་ལྫོ་སྫོ་ལྫོ།;སེམས་ཏན་ཏན་མེད་འགྱོ་བ།
abarticulation;ཚིགས་དཀྲུག་པ།;རྐངམ་དང་ལག་པའི་ཚིགས་དཀྲུག་ི།


# read dictionary(oc_resolved).csv extract English Term;Dzongkha Term;Dzongkha Explanation to english_terms

"""

import json
# from newapi.page import NEW_API
from tqdm import tqdm
from newapi.page import MainPage
# from newapi.wd_sparql import get_query_result
from pathlib import Path

from newapi.api_utils import wd_sparql
from himo_api.himoAPI import wdapi_new

Dir = Path(__file__).parent

# api = NEW_API('en', family='wikipedia')
# api.Login_to_wiki()

qids_file = Dir / "qids.json"
data_file = Dir / "data.json"

results = json.loads(qids_file.read_text('utf-8')) if qids_file.exists() else {}
to_add = json.loads(data_file.read_text('utf-8')) if data_file.exists() else []


def dump_data():

    with open(qids_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


def get_qids(english_terms_new):

    for term in tqdm(english_terms_new, desc="Processing terms"):
        page = MainPage(term, 'en', family='wikipedia')
        if page.exists():
            qid = page.get_qid()  # يحصل على معرف Wikidata
            if qid:
                print(f"{term}: {qid}")
                results[term] = qid

    dump_data()


def get_english_terms():

    english_terms = to_add.keys()

    print(f"len of english_terms: {len(english_terms)}")

    english_terms_new = [x for x in english_terms if x.strip() not in results]
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


def search_wd(english_terms_new):
    # results = wd_sparql.get_query_result(query)
    for term in tqdm(english_terms_new, desc="Processing terms"):
        # ---
        results.setdefault(term, {})
        # ---
        json1 = wdapi_new.wbsearchentities(term, "en") or {}
        # ---
        # print(json1)
        # ---
        # {'Q56690849': {'label': 'abaliénation s. f.', 'lang': 'fr'}, 'Q305266': {'label': 'Abalienation', 'lang': 'en'}}
        # ---
        for qid, data in json1.items():
            # ---
            label = data.get("label")
            lang = data.get("lang")
            # ---
            if label.lower() != term.lower():
                continue
            # ---
            if lang != "en":
                continue
            # ---
            print(f"{label}: {lang} {qid}")
            # ---
            results[term].append(qid)
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


if __name__ == '__main__':
    start()
