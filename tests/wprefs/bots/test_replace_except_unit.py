import re
import unittest

import pywikibot
from wprefs.bots.replace_except import replaceExcept


class DefaultDrySiteTestCase:
    """A base test case with a default dry site."""

    def setup_method(self):
        """Set up a default dry site for testing."""
        self.site = pywikibot.Site("en", "wikipedia")

    def wrap_replaceExcept(self, text, old, new, exceptions, **kwargs):
        """Helper method to call replaceExcept with the default site."""
        return replaceExcept(text, old, new, exceptions, site=self.site, **kwargs)


class TestReplaceExcept(DefaultDrySiteTestCase):
    """Test to verify the replacements with exceptions are done correctly."""

    def test_no_replace(self):
        """Test replacing when the old text does not match."""
        assert self.wrap_replaceExcept("12345678", "x", "y", []) == "12345678"

    def test_simple_replace(self):
        """Test replacing without regex."""
        assert self.wrap_replaceExcept("AxB", "x", "y", []) == "AyB"
        assert self.wrap_replaceExcept("AxxB", "x", "y", []) == "AyyB"
        assert self.wrap_replaceExcept("AxyxB", "x", "y", []) == "AyyyB"

    def test_regex_replace(self):
        """Test replacing with a regex."""
        assert self.wrap_replaceExcept("A123B", r"\d", r"x", []) == "AxxxB"
        assert self.wrap_replaceExcept("A123B", r"\d+", r"x", []) == "AxB"
        assert self.wrap_replaceExcept("A123B", r"A(\d)2(\d)B", r"A\1x\2B", []) == "A1x3B"
        assert self.wrap_replaceExcept("", r"(a?)", r"\1B", []) == "B"
        assert self.wrap_replaceExcept("abc", r"x*", r"-", []) == "-a-b-c-"

        # This is different from re.sub() as re.sub() doesn't
        # allow None groups

        assert self.wrap_replaceExcept("", r"(a)?", r"\1\1", []) == ""

        assert self.wrap_replaceExcept("A123B", r"A(\d)2(\d)B", r"A\g<1>x\g<2>B", []) == "A1x3B"
        assert self.wrap_replaceExcept("A123B", r"A(?P<a>\d)2(?P<b>\d)B", r"A\g<a>x\g<b>B", []) == "A1x3B"
        assert self.wrap_replaceExcept("A123B", r"A(?P<a>\d)2(\d)B", r"A\g<a>x\g<2>B", []) == "A1x3B"
        assert self.wrap_replaceExcept("A123B", r"A(?P<a>\d)2(\d)B", r"A\g<a>x\2B", []) == "A1x3B"
        # test regex with lookbehind.
        assert self.wrap_replaceExcept("A behindB C", r"(?<=behind)\w", r"Z", []) == "A behindZ C"
        # test regex with lookbehind and groups.
        assert self.wrap_replaceExcept(replaceExcept("A behindB C D", r"(?<=behind)\w( )", r"\g<1>Z", []), "A behind ZC D")
        # test regex with lookahead.
        assert self.wrap_replaceExcept("A Bahead C", r"\w(?=ahead)", r"Z", []) == "A Zahead C"
        # test regex with lookahead and groups.
        assert self.wrap_replaceExcept(
            "A Bahead C D", r"( )\w(?=ahead)", r"Z\g<1>", []
        ) == "AZ ahead C D"

    def test_case_sensitive(self):
        """Test replacing with different case sensitivity."""
        assert self.wrap_replaceExcept("AxB", "x", "y", [], caseInsensitive=False) == "AyB"
        assert self.wrap_replaceExcept("AxB", "X", "y", [], caseInsensitive=False) == "AxB"
        assert self.wrap_replaceExcept("AxB", "x", "y", [], caseInsensitive=True) == "AyB"
        assert self.wrap_replaceExcept("AxB", "X", "y", [], caseInsensitive=True) == "AyB"

    def test_replace_with_marker(self):
        """Test replacing with a marker."""
        assert self.wrap_replaceExcept("AxyxB", "x", "y", [], marker=".") == "Ayyy.B"
        assert self.wrap_replaceExcept("AxyxB", "1", "y", [], marker=".") == "AxyxB."

    def test_overlapping_replace(self):
        """Test replacing with and without overlap."""
        assert self.wrap_replaceExcept("1111", "11", "21", [], allowoverlap=False) == "2121"
        assert self.wrap_replaceExcept("1111", "11", "21", [], allowoverlap=True) == "2221"
        self.assertEqual(replaceExcept("1\n= 1 =\n", "1", " \n= 1 =\n", ["header"], allowoverlap=True), " \n= 1 =\n\n= 1 =\n", )

    def test_replace_exception(self):
        """Test replacing not inside a specific regex."""
        assert self.wrap_replaceExcept("123x123", "123", "000", []) == "000x000"
        assert self.wrap_replaceExcept("123x123", "123", "000", [re.compile(r"\w123")]) == "000x123"
        self.assertEqual(replaceExcept("1\n= 1 =\n", "1", "verylongreplacement", ["header"]), "verylongreplacement\n= 1 =\n", )

    def test_replace_tags(self):
        """Test replacing not inside various tags."""
        assert self.wrap_replaceExcept("A <!-- x --> B", "x", "y", ["comment"]) == "A <!-- x --> B"
        assert self.wrap_replaceExcept("\n==x==\n", "x", "y", ["header"]) == "\n==x==\n"
        self.assertEqual(replaceExcept("\n<!--\ncomment-->==x==<!--comment\n-->\n", "x", "y", ["header"]), "\n<!--\ncomment-->==x==<!--comment\n-->\n", )
        assert self.wrap_replaceExcept("<pre>x</pre>", "x", "y", ["pre"]) == "<pre>x</pre>"

        # T191559
        self.assertEqual(replaceExcept("<nowiki   >x</nowiki    >x", "x", "y", ["nowiki"]), "<nowiki   >x</nowiki    >y", )
        self.assertEqual(replaceExcept('<source lang="xml">x</source>', "x", "y", ["source"]), '<source lang="xml">x</source>', )
        self.assertEqual(
            replaceExcept("<syntaxhighlight>x</syntaxhighlight>", "x", "y", ["source"]),
            "<syntaxhighlight>x</syntaxhighlight>",
        )
        self.assertEqual(replaceExcept('<syntaxhighlight lang="xml">x</syntaxhighlight>', "x", "y", ["source"]), '<syntaxhighlight lang="xml">x</syntaxhighlight>', )
        self.assertEqual(replaceExcept("<source>x</source>", "x", "y", ["syntaxhighlight"]), "<source>x</source>")
        self.assertEqual(replaceExcept("<includeonly>x</includeonly>", "x", "y", ["includeonly"]), "<includeonly>x</includeonly>", )
        assert self.wrap_replaceExcept("<ref>x</ref>", "x", "y", ["ref"]) == "<ref>x</ref>"
        self.assertEqual(replaceExcept('<ref name="x">A</ref>', "x", "y", ["ref"]), '<ref name="x">A</ref>')
        assert self.wrap_replaceExcept(" xA ", "x", "y", ["startspace"]) == " xA "
        assert self.wrap_replaceExcept(":xA ", "x", "y", ["startcolon"]) == ":xA "
        assert self.wrap_replaceExcept("<table>x</table>", "x", "y", ["table"]) == "<table>x</table>"
        self.assertEqual(replaceExcept("x [http://www.sample.com x]", "x", "y", ["hyperlink"]), "y [http://www.sample.com y]", )
        self.assertEqual(replaceExcept("x http://www.sample.com/x.html", "x", "y", ["hyperlink"]), "y http://www.sample.com/x.html", )
        self.assertEqual(replaceExcept("<gallery>x</gallery>", "x", "y", ["gallery"]), "<gallery>x</gallery>")
        assert self.wrap_replaceExcept("[[x]]", "x", "y", ["link"]) == "[[x]]"
        self.assertEqual(replaceExcept("{{#property:p171}}", "1", "2", ["property"]), "{{#property:p171}}")
        assert self.wrap_replaceExcept("{{#invoke:x}}", "x", "y", ["invoke"]) == "{{#invoke:x}}"
        self.assertEqual(replaceExcept("<ref name=etwa /> not_in_ref <ref> in_ref </ref>", "not_in_ref", "text", ["ref"]), "<ref name=etwa /> text <ref> in_ref </ref>", )
        assert self.wrap_replaceExcept("<ab> content </a>", "content", "text", ["a"]) == "<ab> text </a>"

    def test_replace_with_count(self):
        """Test replacing with count argument."""
        assert self.wrap_replaceExcept("x [[x]] x x", "x", "y", []) == "y [[y]] y y"
        assert self.wrap_replaceExcept("x [[x]] x x", "x", "y", [], count=5) == "y [[y]] y y"
        assert self.wrap_replaceExcept("x [[x]] x x", "x", "y", [], count=2) == "y [[y]] x x"
        assert self.wrap_replaceExcept("x [[x]] x x", "x", "y", ["link"], count=2) == "y [[x]] y x"

    def test_replace_tag_category(self):
        """Test replacing not inside category links."""
        for ns_name in self.site.namespaces[14]:
            self.assertEqual(
                replaceExcept(f"[[{ns_name}:x]]", "x", "y", ["category"]), f"[[{ns_name}:x]]"
            )

    def test_replace_tag_file(self):
        """Test replacing not inside file links."""
        for ns_name in self.site.namespaces[6]:
            self.assertEqual(replaceExcept(f"[[{ns_name}:x]]", "x", "y", ["file"]), f"[[{ns_name}:x]]")

        assert self.wrap_replaceExcept("[[File:x|foo]]", "x", "y", ["file"]) == "[[File:x|foo]]"

        assert self.wrap_replaceExcept("[[File:x|]]", "x", "y", ["file"]) == "[[File:x|]]"

        self.assertEqual(
            replaceExcept("[[File:x|foo|bar x]] x", "x", "y", ["file"]), "[[File:x|foo|bar x]] y"
        )

        self.assertEqual(
            replaceExcept("[[File:x|]][[File:x|foo]]", "x", "y", ["file"]), "[[File:x|]][[File:x|foo]]"
        )

        assert self.wrap_replaceExcept("[[NonFile:x]]", "x", "y", ["file"]) == "[[NonFile:y]]"

        assert self.wrap_replaceExcept("[[File:]]", "File:", "NonFile:", ["file"]) == "[[File:]]"

        self.assertEqual(
            replaceExcept("[[File:x|[[foo]].]]", "x", "y", ["file"]), "[[File:x|[[foo]].]]"
        )

        # ensure only links inside file are captured
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]].x]][[x]]", "x", "y", ["file"]), "[[File:a|[[foo]].x]][[y]]"
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]][[bar]].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]][[bar]].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]][[bar]].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]][[bar]].x]][[y]]",
        )

        # Correctly handle single brackets in the text.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [bar].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]] [bar].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[bar] [[foo]] .x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[bar] [[foo]] .x]][[y]]",
        )

    def test_replace_tag_file_invalid(self):
        """Test replacing not inside file links with invalid titles."""
        # Correctly handle [ and ] inside wikilinks inside file link
        # even though these are an invalid title.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [invalid] ]].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]] [[bar [invalid] ]].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [invalid ]].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]] [[bar [invalid ]].x]][[y]]",
        )

    @unittest.expectedFailure
    def test_replace_tag_file_failure(self):
        """Test showing limits of the file link regex."""
        # When the double brackets are unbalanced, the regex
        # does not correctly detect the end of the file link.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [[invalid ]].x]][[x]]", "x", "y", ["file"]),
            "[[File:a|[[foo]] [[bar [invalid] ]].x]][[y]]",
        )

    def test_replace_tags_interwiki(self):
        """Test replacing not inside interwiki links."""
        if "es" not in self.site.family.langs or "ey" in self.site.family.langs:
            raise unittest.SkipTest(f"family {self.site} doesn't have languages")

        self.assertEqual(
            replaceExcept("[[es:s]]", "s", "t", ["interwiki"]), "[[es:s]]"
        )  # "es" is a valid interwiki code
        self.assertEqual(
            replaceExcept("[[ex:x]]", "x", "y", ["interwiki"]), "[[ey:y]]"
        )  # "ex" is not a valid interwiki code

    def test_replace_template(self):
        """Test replacing not inside templates."""
        template_sample = r"a {{templatename     | accessdate={{Fecha|1993}}     |atitle=The [[real title]] }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"]), "X" + template_sample[1:]
        )

        template_sample = r"a {{templatename     | 1={{a}}2{{a}}     | 2={{a}}1{{a}} }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"]), "X" + template_sample[1:]
        )

        template_sample = r"a {{templatename     | 1={{{a}}}2{{{a}}}     | 2={{{a}}}1{{{a}}} }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"]), "X" + template_sample[1:]
        )

        # sf.net bug 1575: unclosed template
        template_sample = template_sample[:-2]
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"]), "X" + template_sample[1:]
        )

    def test_replace_source_reference(self):
        """Test replacing in text which contains back references."""
        # Don't use a valid reference number in the original string,
        # in case it tries to apply that as a reference.
        assert replaceExcept(r"\42", r"^(.*)$", r"X\1X", []) == r"X\42X"
        assert replaceExcept(r"\g<bar>", r"^(?P<foo>.*)$", r"X\g<foo>X", []) == r"X\g<bar>X"
