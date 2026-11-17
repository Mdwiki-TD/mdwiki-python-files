#!/usr/bin/python3
"""
إنشاء قائمة بالاهمية من الانجليزية
وحفظها في قاعدة البيانات
"""

import logging
import re
import tqdm

from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.bots.en_to_md import enwiki_to_mdwiki
from mdwiki_api.wiki_page import newapi

logger = logging.getLogger(__name__)

api_new = newapi("en", family="wikipedia")

fals_ase = ["", "na", "unknown"]


logger = logging.getLogger(__name__)


def insert_dict(
    list_of_lines,
    table_name: str,
    columns: list[str],
    lento: int = 10,
) -> None:

    logger.info(f"insert_dict({table_name}): list_of_lines: {len(list_of_lines)}")

    if not list_of_lines:
        return

    done = 0

    co_line = ", ".join(columns)
    values_line = ", ".join(["%s"] * len(columns))

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        tab = list_of_lines[i : i + lento]

        values = []

        for vav in tab:
            values_k = [vav.get(x, "") for x in columns]

            values_2 = []

            for value in values_k:
                values_2.append(value)

            values_2 = tuple(values_2)

            values.append(values_2)

        qua = f"""
            INSERT INTO {table_name} ({co_line})
            values ({values_line})
            """

        sql_for_mdwiki.mdwiki_sql_update(qua, values=values, many=True)

        done += len(tab)

        logger.info(f"to_sql.py insert_dict({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def update_table_2(
    list_of_lines,
    table_name: str,
    columns_to_set: list[str] | None = None,
    lento: int = 10,
    columns_where: list[str] | None = None,
) -> None:

    columns_to_set = columns_to_set or []
    columns_where = columns_where or []

    logger.info(f"update_table_2({table_name}): list_of_lines: {len(list_of_lines)}")

    done = 0

    for i in tqdm.tqdm(range(0, len(list_of_lines), lento)):
        tab = list_of_lines[i : i + lento]

        for vav in tab:
            values = [vav.get(x, "") for x in columns_to_set]

            set_line = ", ".join([f"{x} = %s" for x in columns_to_set])

            qua = f""" update {table_name} set {set_line} where """ + " and ".join([f"{x} = %s" for x in columns_where])

            values.extend([vav[x] for x in columns_where])

            sql_for_mdwiki.mdwiki_sql_update(qua, values=values)

        done += len(tab)

        logger.info(f"to_sql.py update_table_2({table_name}) {done} done, from {len(list_of_lines)} | batch: {lento}.")


def fetch_page_assessments(en_keys: list[str]) -> dict[str, str]:

    data: dict[str, str] = {}
    # من ميد إلى الإنجليزية
    # listo = [mdwiki_to_enwiki.get(cc, cc) for cc in en_keys]

    en_keys = [re.sub(r"^Video:", "Wikipedia:VideoWiki/", x, flags=re.IGNORECASE) for x in en_keys]

    lenn = 0

    for i in range(0, len(en_keys), 50):
        group = en_keys[i : i + 50]

        logger.info(f"get_page_assessments: len of group: {len(group)}")

        result = api_new.get_page_assessments("|".join(group))

        ase = {x["title"]: x for x in result}

        for title, tabe in ase.items():
            # {'pageid': 3186837, 'ns': 0, 'title': 'WAGR syndrome', 'pageassessments': {'Medicine': {'class': 'Start', 'importance': 'Low'}}}

            importance = tabe.get("pageassessments", {}).get("Medicine", {}).get("importance", "")

            if importance.lower() in fals_ase and title.startswith("Wikipedia:VideoWiki/"):
                importance = tabe.get("pageassessments", {}).get("Videowiki", {}).get("importance", "")

            title = title.replace("Wikipedia:VideoWiki/", "Video:")

            # من الإنجليزية إلى ميد
            title = enwiki_to_mdwiki.get(title, title)

            if importance.lower() in fals_ase:
                continue

            lenn += 1 if importance else 0

            data[title] = importance

    logger.info(f"len of new assessments:{lenn}")

    return data


def check_it(x, y, old_values) -> bool:

    if not old_values.get(x):
        return True

    if old_values.get(x, "").lower() in fals_ase:
        return True

    return False


def start_to_sql(data: dict[str, str], from_sql: dict[str, str]) -> None:
    table_name = "assessments"
    columns = ["title", "importance"]

    new_data_insert = [{"title": x, "importance": v} for x, v in data.items() if x not in from_sql]

    new_data_update = [
        {"title": x, "importance": v} for x, v in data.items() if x in from_sql and not check_it(x, v, from_sql)
    ]

    insert_dict(
        list_of_lines=new_data_insert,
        table_name=table_name,
        columns=columns,
    )

    update_table_2(
        list_of_lines=new_data_update,
        table_name=table_name,
        columns_to_set=["importance"],
        lento=100,
        columns_where=["title"],
    )


def main() -> None:

    article_id_list = sql_for_mdwiki.mdwiki_sql_dict("select DISTINCT article_id from category_members")

    all_titles = [x["article_id"] for x in article_id_list]

    in_sql = sql_for_mdwiki.mdwiki_sql_dict("select DISTINCT title, importance from assessments")
    from_sql = {x["title"]: x["importance"] for x in in_sql}

    logger.info(f"len of all_titles: {len(all_titles)}, assessments table: {len(from_sql)}")

    logger.info(f"<<green>> len old assessments {len(from_sql)}")

    data = fetch_page_assessments(all_titles)

    start_to_sql(data, from_sql)


if __name__ == "__main__":
    main()
