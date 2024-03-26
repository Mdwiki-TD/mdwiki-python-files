"""
Usage:

python3 core8/pwb.py p11143_bot/bot -others
python3 core8/pwb.py p11143_bot/bot -td


from p11143_bot import bot as p143_bot
# p143_bot.duplicate(merge_qids)
# p143_bot.add_P11143_to_qids(newlist)
# p143_bot.fix(merge_qids, qids)
# in_wd = p143_bot.make_in_wd_tab()
# p143_bot.add_q(new_qids)

"""
import sys
import time
# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import sql_qids_others
from mdpy.bots import wikidataapi
from mdpy import printe
from mdpy.bots import catdepth2
# ---
sys.argv.append('workhimo')
# ---
wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php")

def add_q(new_qids):
    # ---
    TD_list = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    print(f'len of new_qids: {len(new_qids)}')
    # ---
    if len(new_qids) < 10:
        print("\n".join([f'{k}:{v}' for k, v in new_qids.items()]))
    # ---
    newtitles_not_td = { title: qid for qid, title in new_qids.items() if title not in TD_list }
    # ---
    newtitles_in_td  = { title: qid for qid, title in new_qids.items() if title in TD_list }
    # ---
    print(f'add_q: {len(newtitles_in_td)=}, {len(newtitles_not_td)=}')
    # ---
    if newtitles_in_td or newtitles_not_td:
        printe.output('<<puruple>> add "addq" to sys.argv to add them to qids')
        # ---
        if 'addq' not in sys.argv:
            return
        # ---
        sql_for_mdwiki.add_titles_to_qids(newtitles_in_td)
        # ---
        sql_qids_others.add_titles_to_qids(newtitles_not_td)
    
def make_in_wd_tab():
    # ---
    in_wd = {}
    # ---
    query = '''select distinct ?item ?prop where { ?item wdt:P11143 ?prop .}'''
    # ---
    wdlist = wikidataapi.sparql_generator_url(query, printq=False, add_date=True)
    # ---
    for wd in wdlist:
        prop = wd['prop']
        # ---
        qid = wd['item'].split('/entity/')[1]
        # ---
        in_wd[qid] = prop
    # ---
    return in_wd

def add_P11143_to_qids(newlist):
    # ---
    print(f'len of newlist: {len(newlist)}')
    # ---
    if len(newlist) > 0:
        # ---
        printe.output(f'<<yellow>>claims to add_P11143_to_qids: {len(newlist.items())}')
        if len(newlist.items()) < 100:
            print("\n".join([f'{k}\t:\t{v}' for k, v in newlist.items()]))
        # ---
        if 'add' not in sys.argv:
            printe.output('<<puruple>> add "add" to sys.argv to add them?')
            return
        # ---
        for n, (q, value) in enumerate(newlist.items(), start=1):
            printe.output(f'<<yellow>> q {n} from {len(newlist)}')
            wikidataapi.Claim_API_str(q, 'P11143', value)
            if n % 30 == 0:
                printe.output(f'<<yellow>> n: {n}')
                time.sleep(5)

def fix(merge_qids, qids):
    # mdwiki != P11143
    # تصحيح قيم الخاصية التي لا تساوي اسم المقالة
    # ---
    for q, wd_value in merge_qids.copy().items():
        md_title = qids.get(q)
        if md_title == wd_value:
            continue
        # ---
        print(f'wd_value:{wd_value} != md_title:{md_title}, qid:{q}')
        # ---
        merge_qids[q] = md_title
        # ---
        # delete the old
        ae = wikidataapi.Get_claim(q, 'P11143', get_claim_id=True)
        if ae:
            for x in ae:
                value = x['value']
                claimid = x['id']
                if value == wd_value:
                    uxx = wikidataapi.Delete_claim(claimid)
                    if uxx:
                        print(f'True.. Deleted {claimid}')
                    else:
                        print(f'Failed to delete {claimid}')
        # ---
        # add the correct claim
        ase = wikidataapi.Claim_API_str(q, 'P11143', md_title)
        if ase:
            print(f'True.. Added P11143:{md_title}')
        else:
            print(f'Failed to add P11143:{md_title}')

def duplicate(merge_qids):
    # ايجاد عناصر ويكي بيانات بها قيمة الخاصية في أكثر من عنصر
    va_tab = {}
    # ---
    for q, va in merge_qids.items():
        # ---
        if va not in va_tab:
            va_tab[va] = []
        # ---
        if q not in va_tab[va]:
            va_tab[va].append(q)
    # ---
    va_tab_x = {k: v for k, v in va_tab.items() if len(v) > 1}
    # ---
    if va_tab_x:
        printe.output(f'<<lightyellow>> len of va_tab_x: {len(va_tab_x)}')
        # ---
        for va, qs in va_tab_x.items():
            print(f'va:{va}, qs:{qs}')
    # ---
    printe.output('<<lightyellow>> duplicate() end...')

def work_qids(qids_list):
    # ---
    in_wd = make_in_wd_tab()
    # ---
    qids = {q: title for title, q in qids_list.items() if q != ''}
    # ---
    new_qids = {q: p for q, p in in_wd.items() if q not in qids.keys() and p not in qids.values()}
    # ---
    print(f'len of in_wd: {len(in_wd)}')
    # ---
    newlist = {q: tt for q, tt in qids.items() if q not in in_wd.keys()}
    # ---
    add_P11143_to_qids(newlist)
    # ---
    # merge_qids = {**newlist, **in_wd}
    merge_qids = {**newlist, **in_wd}
    # ---
    if 'fix' in sys.argv:
        fix(merge_qids, qids)
    # ---
    duplicate(merge_qids)
    # ---
    add_q(new_qids)

def start():
    # ---
    if "-others" in sys.argv:
        qids_list = sql_qids_others.get_others_qids()
    else:
        qids_list = sql_for_mdwiki.get_all_qids()
    # ---
    work_qids(qids_list)

if __name__ == '__main__':
    start()
