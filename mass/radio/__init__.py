'''

python3 core8/pwb.py mass/radio/cases_in_ids

tfj run getnewurls --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/geturlsnew"

python3 core8/pwb.py mass/radio/syss/add_syss

python3 core8/pwb.py mass/radio/bots/fix_ids

python3 core8/pwb.py mass/radio/urls_to_get_info

tfj run getids10 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos"

python3 core8/pwb.py mass/radio/to_work

python3 core8/pwb.py mass/radio/studies

python3 core8/pwb.py mass/radio/start

tfj run stz1 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:1"
tfj run stz2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:2"
tfj run stz3 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:3"
tfj run stz4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:4"

tfj run start --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start"
tfj run studies --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos && $HOME/local/bin/python3 core8/pwb.py mass/radio/studies"


'''
