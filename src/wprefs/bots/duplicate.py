#!/usr/bin/python3
""" """

from __future__ import annotations

import itertools
import logging
import re
from contextlib import suppress
from dataclasses import dataclass, field

from pywikibot.textlib import replaceExcept

logger = logging.getLogger(__name__)


@dataclass
class RefData:
    """Data collected for a single distinct reference content."""

    name: str | None = None
    reflist: list[str] = field(default_factory=list)
    quoted: bool = False
    change_needed: bool = False


@dataclass
class ReplacementData:
    """Data needed to fix a <ref name=.../> that pointed to a name
    which got reassigned to different content."""

    name: str
    quoted: bool


def get_html_attributes_value(text: str, param) -> str:
    # rar = r'(?i){0}\s*=\s*[\'"]?(?P<{0}>[^\'" >]+)[\'"]?'.format(param)
    rar = r'(?i){0}\s*=\s*[\'"]?(?P<' + param + r'>[^\'">]+)[\'"]?'
    if not text:
        return ""
    m = re.search(rar, text)
    if m:
        return m.group(param)
    return ""


def get_attrs(text: str) -> dict:
    text = f"<ref {text}>"
    attrfind_tolerant = re.compile(
        r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*'
    )
    attrs = {}
    m = attrfind_tolerant.finditer(text)
    if m:
        for i in m:
            attr_name = i.group(1).lower()
            attr_value = i.group(3) or ""
            attrs[attr_name] = attr_value
    return attrs


def remove_quotes(a):
    if a[:1] == "'" == a[-1:] or a[:1] == '"' == a[-1:]:
        return a[1:-1]
    return a


class DuplicateReferencesBot:
    """Bot to fix duplicate references."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.found_refs: dict[str, dict[str, RefData]] = {}
        self.found_ref_names: dict[str, set] = {}
        self.named_repl: dict[str, ReplacementData] = {}

        # self.autogen = "مولد تلقائيا"
        self.autogen = "autogen"

    def load_data(self) -> None:
        # ---
        # match references
        refs = re.compile(r"(?is)<ref(?P<params>[^>\/]*)>(?P<content>.*?)<\/ref>")
        # ---
        for m in refs.finditer(self.text):
            content = m.group("content")
            # ---
            if not content.strip():
                logger.info("no content")
                continue
            # ---
            params = m.group("params")
            attrs = get_attrs(params)
            # ---
            name_attr = attrs.get("name", "")
            # ---
            group_attr = remove_quotes(attrs.get("group", ""))
            # ---
            is_quoted = False
            # ---
            if name_attr and name_attr[:1] in "'\"":
                name_attr = remove_quotes(name_attr)
                is_quoted = True
            # ---
            self.found_refs.setdefault(group_attr, {})
            self.found_ref_names.setdefault(group_attr, set())
            # ---
            if content in self.found_refs[group_attr]:
                ref_data = self.found_refs[group_attr][content]
                ref_data.reflist.append(m.group())
            else:
                ref_data = RefData(reflist=[m.group()])
            # ---
            if name_attr:
                if not ref_data.name:
                    # First name associated with this content
                    if name_attr not in self.found_ref_names[group_attr]:
                        # first time ever we meet this name
                        ref_data.quoted = is_quoted
                        ref_data.name = name_attr
                    else:
                        # if has_key, means that this name is used
                        # with another content. We'll need to change it
                        ref_data.change_needed = True
                elif ref_data.name != name_attr:
                    self.named_repl[name_attr] = ReplacementData(
                        name=ref_data.name,
                        quoted=ref_data.quoted,
                    )
                # ---
                self.found_ref_names[group_attr].add(name_attr)
            # ---
            self.found_refs[group_attr][content] = ref_data

    def get_free_number(self):
        used_numbers = set()
        for _go, tr in self.found_ref_names.items():
            for name_attr in tr:
                number = name_attr.removeprefix(self.autogen)
                with suppress(ValueError):
                    used_numbers.add(int(number))

        # generator to give the next free number for autogenerating names
        free_number = (str(i) for i in itertools.count(start=1) if i not in used_numbers)
        return free_number

    def fix_found_refs(self, free_number) -> str:
        text = self.text
        for groupname, references in self.found_refs.items():
            group = f'group="{groupname}" ' if groupname else ""

            for ref, ref_data in references.items():
                if len(ref_data.reflist) == 1 and not ref_data.change_needed:
                    continue

                name_attr = ref_data.name
                if not name_attr:
                    name_attr = f'"{self.autogen}{next(free_number)}"'
                elif ref_data.quoted:
                    name_attr = f'"{name_attr}"'

                named = f"<ref {group}name={name_attr}>{ref}</ref>"
                text = text.replace(ref_data.reflist[0], named, 1)

                # make sure that the first (named ref) is not removed later
                pos = text.index(named) + len(named)  # ValueError: substring not found
                header = text[:pos]
                end = text[pos:]

                # replace multiple identical references with repeated ref
                repeated_ref = f"<ref {group}name={name_attr} />"
                for ref in ref_data.reflist[1:]:
                    # Don't replace inside templates (T266411)
                    end = replaceExcept(end, re.escape(ref), repeated_ref, exceptions=["template"])
                text = header + end
        return text

    def fix_refs_with_diff_names(self, text: str) -> str:
        for ref, tag_data in self.named_repl.items():
            # TODO : Support ref groups
            name_attr = tag_data.name
            if tag_data.quoted:
                name_attr = f'"{name_attr}"'

            ref_n = re.escape(ref)
            text = re.sub(
                rf'<ref name\s*=\s*(?P<quote>["\']?)\s*{ref_n}\s*(?P=quote)\s*/>',
                f"<ref name={name_attr} />",
                text,
            )

        return text

    def run(self) -> str:
        # ---
        self.load_data()
        # ---
        logger.info(f"found {len(self.found_ref_names)} in found_ref_names.")
        # ---
        # Find used autogenerated numbers
        free_number = self.get_free_number()
        # ---
        # Fix references
        self.text = self.fix_found_refs(free_number)
        # ---
        # Fix references with different names
        self.text = self.fix_refs_with_diff_names(self.text)
        # ---
        return self.text


def duplicate_references(text: str) -> str:
    return DuplicateReferencesBot(text).run()


__all__ = [
    "duplicate_references",
]
