
#!/bin/bash
# tfj run runviews --image tf-python39 --command "$HOME/pybot/md_core/update_med_views/run.sh"

# $HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:1000
# $HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:5000
# $HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:10000
# $HOME/local/bin/python3 core8/pwb.py update_med_views/bot

$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -max:1000
$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:1000 -max:5000
$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:5000 -max:10000
$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:10000 -max:19000
$HOME/local/bin/python3 core8/pwb.py update_med_views/views_all_run start -min:19000
