
from apis import wikidataapi


def wbsearchentities(search, language):
    return wikidataapi.wbsearchentities(search, language)


def Labels_API(qid, label, lang):
    return wikidataapi.Labels_API(qid, label, lang)


def Des_API(qid, desc, lang):
    return wikidataapi.Des_API(qid, desc, lang)
