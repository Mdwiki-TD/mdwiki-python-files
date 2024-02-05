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

tfj run sta1 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:1 2805"
tfj run sta2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:2 2805"
tfj run sta3 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:3 2805"
tfj run sta4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:4 2805"
tfj run sta5 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:5 2805"
tfj run sta6 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:6 2805"
tfj run sta7 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:7 2805"
tfj run sta8 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:8 2805"
tfj run sta9 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:9 2805"
tfj run sta10 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:10 2805"
tfj run sta11 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:11 2805"
tfj run sta12 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:12 2805"
tfj run sta13 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:13 2805"
tfj run sta14 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:14 12"

tfj run start --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start"
tfj run studies --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_infos && $HOME/local/bin/python3 core8/pwb.py mass/radio/studies"


'''
