#!/usr/bin/python3
"""
Count references and words (in the lead and in the whole article) for every
mdwiki article, and store the counts in the `refs_counts` and `words` tables.

python3 c9/pwb.py td_core/mdcount/countrefs_and_words newpages

python3 c9/pwb.py td_core/mdcount/countrefs_and_words -title:Esophageal_rupture

USED IN mdwiki-jobs.yaml
"""

from __future__ import annotations

import logging
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import tqdm
import wikitextparser as wtp
from db.mdapi_sql.services import sql_for_mdwiki
from md_core_helps.apis import mdwiki_api_call
from td_core.mdcount.bots.wtp_refs import WtpRefs

logger = logging.getLogger(__name__)

SQL_BATCH_SIZE = 100


@dataclass
class TitleCount:
    all: int
    lead: int


@dataclass
class TitleInfo:
    title: str
    words: TitleCount
    refs: TitleCount

    @classmethod
    def load(cls, title: str, text: str) -> TitleInfo:
        lead_section = wtp.parse(text).get_sections(level=0)[0].contents

        # =====================
        # Words

        lead_words = count_text(lead_section)
        full_words = count_text(text)

        logger.info(f"<<green>> all:{full_words} \t lead:{lead_words}")

        # =====================
        # Refs
        refs_all_count = len(WtpRefs.load(text).full_refs)
        refs_lead_count = len(WtpRefs.load(lead_section).all_refs)

        return cls(
            title=title,
            words=TitleCount(all=full_words, lead=lead_words),
            refs=TitleCount(all=refs_all_count, lead=refs_lead_count),
        )

    @property
    def word_table(self) -> dict[str, str | int]:
        return {
            "w_title": self.title,
            "w_lead_words": self.words.lead,
            "w_all_words": self.words.all,
        }

    @property
    def ref_table(self) -> dict[str, str | int]:
        return {
            "r_title": self.title,
            "r_lead_refs": self.refs.lead,
            "r_all_refs": self.refs.all,
        }


def _plain(text: str) -> str:
    return wtp.parse(text).plain_text()


def _template_to_text(template: wtp.Template) -> str:
    """Flatten a template into its non-empty argument values, one per bullet."""
    values = (_plain(arg.value.strip()) for arg in template.arguments if arg.value and arg.value.strip())

    return "\n* ".join(v.strip() for v in values if v.strip())


def count_text(text: str) -> int:
    """Count the words in wikitext, ignoring tags (such as refs) and numbers."""
    parsed = wtp.parse(text)

    for tag in parsed.get_tags():
        tag.string = ""

    plain = wtp.parse(parsed.string).plain_text(replace_templates=_template_to_text)

    plain = re.sub(r"\d+", "", plain)

    return len(re.findall(r"\w+", plain))


def batched(items: list, size: int) -> Iterator[list]:
    """Yield successive slices of items, showing a progress bar."""
    for start in tqdm.tqdm(range(0, len(items), size)):
        yield items[start : start + size]


def sync_table(
    table_name: str,
    key_column: str,
    value_columns: list[str],
    rows: list[dict[str, Any]],
    existing: list[dict[str, Any]],
) -> None:
    """Insert rows missing from the table, and update rows whose values changed."""
    columns = [key_column, *value_columns]

    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    set_line = ", ".join(f"{col} = %s" for col in value_columns)
    update_query = f"UPDATE {table_name} SET {set_line} WHERE {key_column} = %s"

    old_by_key = {row[key_column]: row for row in existing}

    to_insert = []
    to_update = []

    # Later duplicates in rows win.
    for key, row in {row[key_column]: row for row in rows}.items():
        old = old_by_key.get(key)

        if old is None:
            to_insert.append(tuple(row[col] for col in columns))
        elif any(str(old.get(col, "")) != str(row[col]) for col in value_columns):
            to_update.append(tuple(row[col] for col in value_columns) + (key,))

    logger.info(f"{table_name}: {len(to_insert)=}, {len(to_update)=}")

    if "nodump" in sys.argv:
        logger.info('"nodump" in sys.argv - no dump')
        return

    for query, values in ((insert_query, to_insert), (update_query, to_update)):
        for batch in batched(values, SQL_BATCH_SIZE):
            sql_for_mdwiki.mdwiki_sql_update(query, values=batch, many=True)


def load_title_infos(titles: list[str]) -> list[TitleInfo]:
    """Download every page and compute its word and reference counts."""
    data: list[TitleInfo] = []

    for numb, title in enumerate(titles):
        title = title.replace("\\'", "'")

        logger.info("------------------")
        logger.info(f"page {numb} from {len(titles)}, x:{title}")

        text = mdwiki_api_call.get_page_text(title)

        data.append(TitleInfo.load(title, text))

    return data

def main() -> None:
    rows = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT article_id FROM category_members")
    all_titles = [x["article_id"] for x in rows]

    data = load_title_infos(all_titles)

    # Read the tables after the slow download so the comparison is fresh.
    words_in_sql = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT w_title, w_lead_words, w_all_words FROM words")
    refs_in_sql = sql_for_mdwiki.mdwiki_sql_dict("SELECT DISTINCT r_title, r_lead_refs, r_all_refs FROM refs_counts")

    # ==============================
    # Words
    sync_table(
        table_name="words",
        key_column="w_title",
        value_columns=["w_lead_words", "w_all_words"],
        rows=[x.word_table for x in data],
        existing=words_in_sql,
    )

    # ==============================
    # Refs
    sync_table(
        table_name="refs_counts",
        key_column="r_title",
        value_columns=["r_lead_refs", "r_all_refs"],
        rows=[x.ref_table for x in data],
        existing=refs_in_sql,
    )


if __name__ == "__main__":
    main()
