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

tfj run start1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:1"
tfj run start2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:2"
tfj run start3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:3"
tfj run start4 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:4"
tfj run start5 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:5"
tfj run start6 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:6"
tfj run start7 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:7"
tfj run start8 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:8"
tfj run start9 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:9"
tfj run start10 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:10"

tfj run start --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start"
tfj run studies --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos && $HOME/local/bin/python3 core8/pwb.py mass/radio/studies"


'''
