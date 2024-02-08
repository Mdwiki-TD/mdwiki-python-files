'''

tfj run chsh --image mariadb --command "$HOME/ch.sh"

python3 core8/pwb.py mass/radio/cases_in_ids

tfj run getnewurls --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/geturlsnew"

python3 core8/pwb.py mass/radio/syss/add_syss

python3 core8/pwb.py mass/radio/bots/fix_ids

python3 core8/pwb.py mass/radio/urls_to_get_info

tfj run getids10 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos"

python3 core8/pwb.py mass/radio/to_work

python3 core8/pwb.py mass/radio/studies

python3 core8/pwb.py mass/radio/start

tfj run rad1 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:1 2226"
tfj run rad2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:2 2226"
tfj run rad3 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:3 2226"
tfj run rad4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:4 2226"
tfj run rad5 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:5 2226"
tfj run rad6 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:6 2226"
tfj run rad7 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:7 2226"
tfj run rad8 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:8 2226"
tfj run rad9 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:9 2226"
tfj run rad10 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:10 2226"
tfj run rad11 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:11 2226"
tfj run rad12 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:12 2226"
tfj run rad13 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:13 2226"
tfj run rad14 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:14 1"


tfj run radrt --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start"
tfj run studies --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos && $HOME/local/bin/python3 core8/pwb.py mass/radio/studies"


'''
