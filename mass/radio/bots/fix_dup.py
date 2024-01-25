'''
python3 core8/pwb.py mass/radio/bots/fix_dup ask
tfj run fixdup1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/bots/fix_dup"

'''
from new_api import printe
from new_api.ncc_page import MainPage as ncc_MainPage, CatDepth
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
empty_cats = []
# ---
for n, (idn, cats) in enumerate(jsons.cases_dup.items(), start=1):
    # ---
    cat1 = cats[0]
    cat2 = cats[1]
    # ---
    if cat1 == cat2:
        continue
    # ---
    printe.output(f'd:s{n}/{len(jsons.cases_dup)}<<lightyellow>> {idn} {cat1} {cat2}')
    # ---
    cat1_page = ncc_MainPage(cat1, 'www', family='nccommons')
    cat2_page = ncc_MainPage(cat2, 'www', family='nccommons')
    # ---
    main_cat = cat1_page
    other_cat = cat2_page
    # ---
    main_title = cat1
    other_title = cat2
    # ---
    cat1_text = cat1_page.get_text()
    cat2_text = cat2_page.get_text()
    # ---
    main_text = cat1_text
    other_text = cat2_text
    # ---
    if cat1_text.find('* [https://radiopaedia.org/cases/') != -1:
        main_cat = cat1_page
        other_cat = cat2_page
        # ---
        main_text = cat1_text
        other_text = cat2_text
        # ---
        main_title = cat1
        other_title = cat2
    elif cat2_text.find('* [https://radiopaedia.org/cases/') != -1:
        main_cat = cat2_page
        other_cat = cat1_page
        # ---
        main_text = cat2_text
        other_text = cat1_text
        # ---
        main_title = cat2
        other_title = cat1
    # ---
    # add other_cat text to main_cat
    new_main_text = f"{main_text}\n{other_text}"
    # ---
    new_main_text = new_main_text.replace(f'| 0{idn}]]', f'|{idn}]]')
    new_main_text = new_main_text.replace(f'|0{idn}]]', f'|{idn}]]')
    new_main_text = new_main_text.replace(f'| {idn}]]', f'|{idn}]]')
    # ---
    # remove duplicate lines from new_main_text
    cc = list(set(new_main_text.split('\n')))
    cc.sort()
    # ---
    # remove '[[Category:cats to delete]]'
    if '[[Category:cats to delete]]' in cc:
        cc.remove('[[Category:cats to delete]]')
    # ---
    new_main_text = '\n'.join([line for line in cc if line.strip()])
    # ---
    empty_cats.append(other_title)
    # ---
    if new_main_text != main_text:
        main_cat.save(newtext=new_main_text, summary=f'from [[{other_title}]]')
    # ---
    cat_files = CatDepth(other_title, sitecode='www', family="nccommons", depth=0, ns="all")
    # ---
    for file in cat_files:
        file_page = ncc_MainPage(file, 'www', family='nccommons')
        file_text = file_page.get_text()
        # ---
        # replace old title by new
        file_newtext = file_text
        file_newtext = file_newtext.replace(f'[[{other_title}]]', f'[[{main_cat.title}]]')
        file_newtext = file_newtext.replace(f'[[{other_title}|', f'[[{main_cat.title}|')
        # ---
        if file_newtext != file_text:
            file_page.save(newtext=file_newtext, summary='update')
    # ---
    cat_files2 = CatDepth(other_title, sitecode='www', family="nccommons", depth=0, ns="all")
    # ---
    if other_cat.exists():
        if len(cat_files2) == 0:
            printe.output(f'<<green>> cat {other_title} is empty.. done..')
            other_cat.save(newtext='[[Category:cats to delete]]', summary='empty cat')
