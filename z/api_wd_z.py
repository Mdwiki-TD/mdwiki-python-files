
fafo_rand = "960017df0e23"  # f"{random.randrange(0, 2 ** 48):x}"

summary = f"([[:toollabs:editgroups/b/CB/{fafo_rand}|details]])"

print(f"summary: {summary}")

from apis import wikidataapi


def wbsearchentities(search, language):
    return wikidataapi.wbsearchentities(search, language)


def Labels_API(qid, label, lang):
    return wikidataapi.Labels_API(qid, label, lang, summary=summary)


def Des_API(qid, desc, lang):
    return wikidataapi.Des_API(qid, desc, lang, summary=summary)
