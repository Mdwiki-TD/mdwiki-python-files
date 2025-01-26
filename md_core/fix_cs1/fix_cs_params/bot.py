#!/usr/bin/python3
"""

python3 core8/pwb.py fix_cs1/fix_cs_params/bot -cat:Category:CS1_errors:_archive-url archive ask
python3 core8/pwb.py fix_cs1/fix_cs_params/bot -cat:Category:RTT fix2 ask
python3 core8/pwb.py fix_cs1/fix_cs_params/bot

tfj run fixrefs1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_cs1/fix_cs_params/bot all"

"""
import sys
import wikitextparser as wtp
from newapi import printe

from newapi.mdwiki_page import MainPage as md_MainPage, CatDepth, NEW_API
from fix_cs1.archive_date_maker import make_archive_date, make_archive_date_and_url

api_new = NEW_API("www", family="mdwiki")

dup_args = {
    "trans-title": [
        "trans_title",
        "trans title",
        "transtitle",
    ],
    "dead-url": [
        "deadurl",
    ],
    "access-date": [
        "accessdate",
        "access date",
        "accessDate",
    ],
    "archive-date": [
        "archivedate",
        "archive date",
    ],
    "archive-url": [
        "archiveurl",
        "archive url",
    ],
    "chapter-url": [
        "chapterurl",
        "chapter url",
    ],
    "url-access": [
        "urlaccess",
        "url access",
    ],
    "author-link": [
        "authorlink",
        "author link",
    ],
    "editor-link": [
        "editorlink",
        "editor link",
    ],
}
old_to_new_params = {}

for new, old in dup_args.items():
    for x in old:
        old_to_new_params[x] = new


def gt_arg(temp, name):
    if temp.has_arg(name):
        va = temp.get_arg(name)
        if va and va.value and va.value.strip():
            return va.value.strip()
    return ""


class AddArchiveDate:
    def __init__(self):
        pass

    def run_archive(self):
        # ---
        newtext = self.fix_it(self.text)
        # ---
        if self.text == newtext:
            return
        # ---
        added_str = ", ".join([f"{k}:{v}" for k, v in self.added.items()])
        # ---
        summary = "Fix reference parameters "
        # ---
        if self.added:
            printe.output(f" >> {self.title} {added_str}")
            # ---
            summary += f" (Add: {added_str})"
        # ---
        self.save_page(newtext, summary)

    def param_added_plus(self, param):
        self.added.setdefault(param, 0)
        self.added[param] += 1

    def archive_param(self, temp):
        # ---
        url = gt_arg(temp, "url")
        archiveurl = gt_arg(temp, "archive-url")
        # ---
        archive_date = gt_arg(temp, "archive-date") or gt_arg(temp, "archivedate")
        # ---
        if archiveurl and not archive_date:
            # ---
            archive_date = make_archive_date(archiveurl)
            # ---
            if archive_date:
                temp.set_arg("archive-date", archive_date)
                # ---
                self.param_added_plus("archive-date")
                # ---
        # ---
        chapterurl = gt_arg(temp, "chapter-url") or gt_arg(temp, "chapterurl")
        # ---
        if not url and archiveurl and not chapterurl:
            found_it, archivedate, n_url, archiveurl = make_archive_date_and_url(archiveurl)
            # ---
            if found_it:
                # ---
                temp.set_arg("url", n_url)
                self.param_added_plus("url")
                # ---
                if not archive_date:
                    temp.set_arg("archive-date", archivedate)
                    self.param_added_plus("archive-date")
                # ---
        # ---
        return temp

    def fix_it(self, text):
        # ---
        parser = wtp.parse(text)
        # ---
        for temp in parser.templates:
            # ---
            temp_str = temp.string
            # ---
            if not temp_str or temp_str.strip() == "":
                continue
            # ---
            self.archive_param(temp)
            # ---
            # temp.rm_dup_args_safe()
        # ---
        text = parser.string
        # ---
        return text


class one_page(AddArchiveDate):
    def __init__(self, title):
        # ---
        super().__init__()
        # ---
        self.title = title
        """Treat one double redirect."""
        # ---
        self.added = {}
        self.replaced = {}
        # ---
        self.removed = {}
        # ---
        self.page = md_MainPage(self.title, "www", family="mdwiki")
        # ---
        if not self.page.exists():
            printe.output(f" page:{self.title} not exists in mdwiki.")
            return
        # ---
        self.text = self.page.get_text()
        # ---
        # if "archive" in sys.argv:
        #     self.run_archive()
        # else:
        #     self.run()
        #     self.run_archive()

    def run(self):
        # ---
        newtext = self.fix_text_2(self.text) # AttributeError: 'one_page' object has no attribute 'text'
        # ---
        if self.text == newtext:
            return
        # ---
        summary = "Fix reference parameters "
        # ---
        if self.replaced:
            replace_str = ", ".join([f"{k}>{old_to_new_params.get(k,k)}({v})" for k, v in self.replaced.items()])
            # ---
            printe.output(f" >> {self.title} {replace_str}")
            # ---
            summary += f"(replace: {replace_str})"
        if self.removed:
            removed_str = ", ".join([f"{k}:{v}" for k, v in self.removed.items()])
            # ---
            printe.output(f" >> {self.title} {removed_str}")
            # ---
            summary += f" (remove: {removed_str})"
        # ---
        self.save_page(newtext, summary)

    def save_page(self, newtext, summary):
        # ---
        if self.text == newtext:
            return
        # ---
        printe.output(f"save: {self.title}")
        # --
        save = self.page.save(newtext=newtext, summary=summary)
        # ---
        if save:
            self.text = newtext

    def one_fix(self, temp, old_p, new_p):
        if temp.has_arg(old_p) and temp.has_arg(new_p):
            # ---
            p1_value = gt_arg(temp, old_p)
            p2_value = gt_arg(temp, new_p)
            # ---
            if not p2_value:
                temp.set_arg(new_p, p1_value)
            # ---
            if p1_value == p2_value:
                printe.output(f"<<yellow>> one_fix: {old_p} && {new_p} == <<green>> ({p1_value})")
            else:
                printe.output(f"<<yellow>> one_fix: |{old_p}={p1_value} && |{new_p}={p2_value}")
            # ---
            printe.output(f"\t <<red>> del {old_p=}")
            # ---
            self.removed.setdefault(old_p, 0)
            self.removed[old_p] += 1
            # ---
            temp.del_arg(old_p)

    def fix_dupls(self, temp):
        for new, old in dup_args.items():
            for x in old:
                self.one_fix(temp, x, new)

    def fix_text_2(self, text):
        # ---
        parser = wtp.parse(text)
        # ---
        for temp in parser.templates:
            # ---
            temp_str = temp.string
            # ---
            if not temp_str or temp_str.strip() == "":
                continue
            # ---
            self.fix_dupls(temp)
            # ---
            # temp.rm_dup_args_safe()
        # ---
        for temp in parser.templates:
            # ---
            temp_str = temp.string
            # ---
            if not temp_str or temp_str.strip() == "":
                continue
            # ---
            changed = False
            # ---
            for arg in temp.arguments:
                # ---
                if arg.name.strip() in old_to_new_params:
                    # ---
                    old_name = arg.name.strip()
                    new_name = old_to_new_params[arg.name.strip()]
                    # ---
                    self.replaced.setdefault(old_name, 0)
                    self.replaced[old_name] += 1
                    # ---
                    arg.name = new_name
                    # ---
                    changed = True
                    continue
                # ---
                if "-" in arg.name.strip() and temp.has_arg(arg.name.strip().replace("-", "")):
                    arg.name = arg.name.strip().replace("-", "")
                    changed = True
            # ---
            if changed:
                temp.rm_dup_args_safe()
        # ---
        text = parser.string
        # ---
        return text


def one_title(title):
    bot = one_page(title)
    # ---
    if "archive" in sys.argv:
        bot.run_archive()
    else:
        bot.run()
        bot.run_archive()


def main():
    printe.output("*<<red>> > main:")
    # ---
    cat = "Category:CS1 errors: redundant parameter"
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        # ---
        if arg.lower() in ["cat", "-cat"] and value.strip():
            cat = value
            break
    # ---
    if "all" in sys.argv:
        titles = api_new.Get_All_pages()
    else:
        printe.output(f"cat: {cat}")
        titles = CatDepth(cat, sitecode="www", family="mdwiki")
    # ---
    if "re" in sys.argv:
        titles = list(reversed(titles))
        # titles.reverse()
    # ---
    for n, page in enumerate(titles):
        printe.output(f"n: {n}/{len(titles)} - Page: {page}")
        # ---
        one_title(page)


if __name__ == "__main__":
    if "test" in sys.argv:
        title = "Urinary_system"
        one_title(title)
    else:
        main()
