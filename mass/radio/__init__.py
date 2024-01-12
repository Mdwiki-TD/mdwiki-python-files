'''

python3 core8/pwb.py mass/radio/cases

python3 core8/pwb.py mass/radio/geturls

python3 core8/pwb.py mass/radio/to_work

python3 core8/pwb.py mass/radio/get_ids

python3 core8/pwb.py mass/radio/studies

python3 core8/pwb.py mass/radio/authors

python3 core8/pwb.py mass/radio/start

tfj run start1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:1"
tfj run start2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:2"
tfj run start3 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:3"
tfj run start4 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start nodiff get:4"

tfj run start --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/start"
tfj run studies --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/get_ids && $HOME/local/bin/python3 core8/pwb.py mass/radio/studies"


'''