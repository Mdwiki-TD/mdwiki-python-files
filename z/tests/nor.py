"""

python3 I:/mdwiki/pybot/z/tests/nor.py


"""


def get_title_redirect_normolize_x(title, redirects, normalized):
    # ---
    tab = {
        "user_input": title,
        "redirect_to": "",
        "normalized_to": ""
    }
    # ---
    if redirects:
        for r in redirects:
            if r.get("to") == tab["user_input"]:
                tab["redirect_to"] = r.get("to", "")
                tab["user_input"] = r.get("from", "")
                break
    # --- تحقق من وجود normalized
    if normalized:
        for n in normalized:
            if n.get("to") == tab["user_input"]:
                tab["normalized_to"] = n.get("to", "")
                tab["user_input"] = n.get("from", "")
                break
    # ---
    return tab


def get_title_redirect_normolize(title, redirects, normalized):
    # ---
    redirects = redirects or []
    normalized = normalized or []
    # ---
    tab = {
        "user_input": title,
        "redirect_to": "",
        "normalized_to": ""
    }
    # ---
    normalized = {x["to"]: x["from"] for x in normalized}
    # ---
    redirects = {x["to"]: x["from"] for x in redirects}
    # ---
    if tab["user_input"] in redirects:
        tab["redirect_to"] = tab["user_input"]
        tab["user_input"] = redirects[tab["user_input"]]
    # ---
    if tab["user_input"] in normalized:
        tab["normalized_to"] = tab["user_input"]
        tab["user_input"] = normalized[tab["user_input"]]
    # ---
    return tab


_example = {
    "warnings": {
        "main": {
            "warnings": "Unrecognized parameters: pplimit, token, bot."
        }
    },
    "query": {
        "redirects": [
            {
                "from": "Arteries",
                "to": "Artery"
            },
            {
                "from": "Acapnia",
                "to": "Hypocapnia"
            }
        ],
        "normalized": [
            {
                "from": "acapnia",
                "to": "Acapnia"
            }
        ],
        "pages": [
            {
                "pageid": 36790,
                "ns": 0,
                "title": "Artery",
                "contentmodel": "wikitext",
                "pagelanguage": "en",
                "pagelanguagehtmlcode": "en",
                "pagelanguagedir": "ltr",
                "touched": "2025-07-31T20:50:54Z",
                "lastrevid": 1291940564,
                "length": 19820,
                "pageprops": {
                    "wikibase_item": "Q9655"
                }
            },
            {
                "pageid": 1063454,
                "ns": 0,
                "title": "Hypocapnia",
                "contentmodel": "wikitext",
                "pagelanguage": "en",
                "pagelanguagehtmlcode": "en",
                "pagelanguagedir": "ltr",
                "touched": "2025-08-04T18:19:22Z",
                "lastrevid": 1292035730,
                "length": 7408,
                "pageprops": {
                    "wikibase_item": "Q1328215"
                }
            }
        ]
    },
    "all_titles": [
        "Arteries",
        "acapnia"
    ]
}

# ---
redirects = _example["query"]["redirects"]
normalized = _example["query"]["normalized"]
# ---
for x in _example["query"]["pages"]:
    title = x["title"]
    # ---
    print(f"__________\n title: {title}")
    real_title = get_title_redirect_normolize(title, redirects, normalized)
    # ---
    print(f"redirect_to: {real_title['redirect_to']}")
    print(f"normalized_to: {real_title['normalized_to']}")
    # ---
    print(f"user_input: {real_title['user_input']}")
