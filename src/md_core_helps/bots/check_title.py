""" """

falses = [
    "category:",
    "file:",
    "template:",
    "user:",
    # "video:",
    "wikipedia:",
]


def valid_title(title: str) -> bool:
    # ---
    title = title.lower().strip()
    # ---
    if title.find("(disambiguation)") != -1:
        return False
    # ---
    # if title.startswith('category:') or title.startswith('file:') or title.startswith('template:') or title.startswith('user:'):
    return not any(title.startswith(prefix) for prefix in falses)
