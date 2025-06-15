
#!/bin/bash
# tfj run umvsh --image tf-python39 --command "$HOME/pybot/md_core/update_med_views/run.sh"

$HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:1000
$HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:5000
$HOME/local/bin/python3 core8/pwb.py update_med_views/bot -max:10000
$HOME/local/bin/python3 core8/pwb.py update_med_views/bot
