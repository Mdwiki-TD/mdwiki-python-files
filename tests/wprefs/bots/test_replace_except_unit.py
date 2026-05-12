import re
import unittest

import pywikibot
from wprefs.bots.replace_except import replaceExcept


class DefaultDrySiteTestCase:
    """A base test case with a default dry site."""

    def setup_method(self):
        """Set up a default dry site for testing."""
        self.site = pywikibot.Site("en", "wikipedia")


class TestReplaceExcept(DefaultDrySiteTestCase):
    """Test to verify the replacements with exceptions are done correctly."""

    def test_no_replace(self):
        """Test replacing when the old text does not match."""
        assert replaceExcept("12345678", "x", "y", [], site=self.site) == "12345678"

    def test_simple_replace(self):
        """Test replacing without regex."""
        assert replaceExcept("AxB", "x", "y", [], site=self.site) == "AyB"
        assert replaceExcept("AxxB", "x", "y", [], site=self.site) == "AyyB"
        assert replaceExcept("AxyxB", "x", "y", [], site=self.site) == "AyyyB"

    def test_regex_replace(self):
        """Test replacing with a regex."""
        assert replaceExcept("A123B", r"\d", r"x", [], site=self.site) == "AxxxB"
        assert replaceExcept("A123B", r"\d+", r"x", [], site=self.site) == "AxB"
        assert replaceExcept("A123B", r"A(\d)2(\d)B", r"A\1x\2B", [], site=self.site) == "A1x3B"
        assert replaceExcept("", r"(a?)", r"\1B", [], site=self.site) == "B"
        assert replaceExcept("abc", r"x*", r"-", [], site=self.site) == "-a-b-c-"

        # This is different from re.sub() as re.sub() doesn't
        # allow None groups

        assert replaceExcept("", r"(a)?", r"\1\1", [], site=self.site) == ""

        assert replaceExcept("A123B", r"A(\d)2(\d)B", r"A\g<1>x\g<2>B", [], site=self.site) == "A1x3B"
        assert replaceExcept("A123B", r"A(?P<a>\d)2(?P<b>\d)B", r"A\g<a>x\g<b>B", [], site=self.site) == "A1x3B"
        assert replaceExcept("A123B", r"A(?P<a>\d)2(\d)B", r"A\g<a>x\g<2>B", [], site=self.site) == "A1x3B"
        assert replaceExcept("A123B", r"A(?P<a>\d)2(\d)B", r"A\g<a>x\2B", [], site=self.site) == "A1x3B"
        # test regex with lookbehind.
        assert replaceExcept("A behindB C", r"(?<=behind)\w", r"Z", [], site=self.site) == "A behindZ C"
        # test regex with lookbehind and groups.
        assert replaceExcept(
            replaceExcept("A behindB C D", r"(?<=behind)\w( )", r"\g<1>Z", [], site=self.site), "A behind ZC D"
        )
        # test regex with lookahead.
        assert replaceExcept("A Bahead C", r"\w(?=ahead)", r"Z", [], site=self.site) == "A Zahead C"
        # test regex with lookahead and groups.
        assert replaceExcept(
            "A Bahead C D", r"( )\w(?=ahead)", r"Z\g<1>", [], site=self.site
        ) == "AZ ahead C D"

    def test_case_sensitive(self):
        """Test replacing with different case sensitivity."""
        assert replaceExcept("AxB", "x", "y", [], caseInsensitive=False, site=self.site) == "AyB"
        assert replaceExcept("AxB", "X", "y", [], caseInsensitive=False, site=self.site) == "AxB"
        assert replaceExcept("AxB", "x", "y", [], caseInsensitive=True, site=self.site) == "AyB"
        assert replaceExcept("AxB", "X", "y", [], caseInsensitive=True, site=self.site) == "AyB"

    def test_replace_with_marker(self):
        """Test replacing with a marker."""
        assert replaceExcept("AxyxB", "x", "y", [], marker=".", site=self.site) == "Ayyy.B"
        assert replaceExcept("AxyxB", "1", "y", [], marker=".", site=self.site) == "AxyxB."

    def test_overlapping_replace(self):
        """Test replacing with and without overlap."""
        assert replaceExcept("1111", "11", "21", [], allowoverlap=False, site=self.site) == "2121"
        assert replaceExcept("1111", "11", "21", [], allowoverlap=True, site=self.site) == "2221"
        self.assertEqual(
            replaceExcept("1\n= 1 =\n", "1", " \n= 1 =\n", ["header"], allowoverlap=True, site=self.site),
            " \n= 1 =\n\n= 1 =\n",
        )

    def test_replace_exception(self):
        """Test replacing not inside a specific regex."""
        assert replaceExcept("123x123", "123", "000", [], site=self.site) == "000x000"
        assert replaceExcept("123x123", "123", "000", [re.compile(r"\w123")], site=self.site) == "000x123"
        self.assertEqual(
            replaceExcept("1\n= 1 =\n", "1", "verylongreplacement", ["header"], site=self.site),
            "verylongreplacement\n= 1 =\n",
        )

    def test_replace_tags(self):
        """Test replacing not inside various tags."""
        assert replaceExcept("A <!-- x --> B", "x", "y", ["comment"], site=self.site) == "A <!-- x --> B"
        assert replaceExcept("\n==x==\n", "x", "y", ["header"], site=self.site) == "\n==x==\n"
        self.assertEqual(
            replaceExcept("\n<!--\ncomment-->==x==<!--comment\n-->\n", "x", "y", ["header"], site=self.site),
            "\n<!--\ncomment-->==x==<!--comment\n-->\n",
        )
        assert replaceExcept("<pre>x</pre>", "x", "y", ["pre"], site=self.site) == "<pre>x</pre>"
        self.assertEqual(
            replaceExcept("<nowiki   >x</nowiki    >x", "x", "y", ["nowiki"], site=self.site),
            "<nowiki   >x</nowiki    >y",
        )  # T191559
        self.assertEqual(
            replaceExcept('<source lang="xml">x</source>', "x", "y", ["source"], site=self.site),
            '<source lang="xml">x</source>',
        )
        self.assertEqual(
            replaceExcept("<syntaxhighlight>x</syntaxhighlight>", "x", "y", ["source"], site=self.site),
            "<syntaxhighlight>x</syntaxhighlight>",
        )
        self.assertEqual(
            replaceExcept('<syntaxhighlight lang="xml">x</syntaxhighlight>', "x", "y", ["source"], site=self.site),
            '<syntaxhighlight lang="xml">x</syntaxhighlight>',
        )
        self.assertEqual(
            replaceExcept("<source>x</source>", "x", "y", ["syntaxhighlight"], site=self.site), "<source>x</source>"
        )
        self.assertEqual(
            replaceExcept("<includeonly>x</includeonly>", "x", "y", ["includeonly"], site=self.site),
            "<includeonly>x</includeonly>",
        )
        assert replaceExcept("<ref>x</ref>", "x", "y", ["ref"], site=self.site) == "<ref>x</ref>"
        self.assertEqual(
            replaceExcept('<ref name="x">A</ref>', "x", "y", ["ref"], site=self.site), '<ref name="x">A</ref>'
        )
        assert replaceExcept(" xA ", "x", "y", ["startspace"], site=self.site) == " xA "
        assert replaceExcept(":xA ", "x", "y", ["startcolon"], site=self.site) == ":xA "
        assert replaceExcept("<table>x</table>", "x", "y", ["table"], site=self.site) == "<table>x</table>"
        self.assertEqual(
            replaceExcept("x [http://www.sample.com x]", "x", "y", ["hyperlink"], site=self.site),
            "y [http://www.sample.com y]",
        )
        self.assertEqual(
            replaceExcept("x http://www.sample.com/x.html", "x", "y", ["hyperlink"], site=self.site),
            "y http://www.sample.com/x.html",
        )
        self.assertEqual(
            replaceExcept("<gallery>x</gallery>", "x", "y", ["gallery"], site=self.site), "<gallery>x</gallery>"
        )
        assert replaceExcept("[[x]]", "x", "y", ["link"], site=self.site) == "[[x]]"
        self.assertEqual(
            replaceExcept("{{#property:p171}}", "1", "2", ["property"], site=self.site), "{{#property:p171}}"
        )
        assert replaceExcept("{{#invoke:x}}", "x", "y", ["invoke"], site=self.site) == "{{#invoke:x}}"
        self.assertEqual(
            replaceExcept(
                "<ref name=etwa /> not_in_ref <ref> in_ref </ref>", "not_in_ref", "text", ["ref"], site=self.site
            ),
            "<ref name=etwa /> text <ref> in_ref </ref>",
        )
        assert replaceExcept("<ab> content </a>", "content", "text", ["a"], site=self.site) == "<ab> text </a>"

    def test_replace_with_count(self):
        """Test replacing with count argument."""
        assert replaceExcept("x [[x]] x x", "x", "y", [], site=self.site) == "y [[y]] y y"
        assert replaceExcept("x [[x]] x x", "x", "y", [], site=self.site, count=5) == "y [[y]] y y"
        assert replaceExcept("x [[x]] x x", "x", "y", [], site=self.site, count=2) == "y [[y]] x x"
        assert replaceExcept("x [[x]] x x", "x", "y", ["link"], site=self.site, count=2) == "y [[x]] y x"

    def test_replace_tag_category(self):
        """Test replacing not inside category links."""
        for ns_name in self.site.namespaces[14]:
            self.assertEqual(
                replaceExcept(f"[[{ns_name}:x]]", "x", "y", ["category"], site=self.site), f"[[{ns_name}:x]]"
            )

    def test_replace_tag_file(self):
        """Test replacing not inside file links."""
        for ns_name in self.site.namespaces[6]:
            self.assertEqual(replaceExcept(f"[[{ns_name}:x]]", "x", "y", ["file"], site=self.site), f"[[{ns_name}:x]]")

        assert replaceExcept("[[File:x|foo]]", "x", "y", ["file"], site=self.site) == "[[File:x|foo]]"

        assert replaceExcept("[[File:x|]]", "x", "y", ["file"], site=self.site) == "[[File:x|]]"

        self.assertEqual(
            replaceExcept("[[File:x|foo|bar x]] x", "x", "y", ["file"], site=self.site), "[[File:x|foo|bar x]] y"
        )

        self.assertEqual(
            replaceExcept("[[File:x|]][[File:x|foo]]", "x", "y", ["file"], site=self.site), "[[File:x|]][[File:x|foo]]"
        )

        assert replaceExcept("[[NonFile:x]]", "x", "y", ["file"], site=self.site) == "[[NonFile:y]]"

        assert replaceExcept("[[File:]]", "File:", "NonFile:", ["file"], site=self.site) == "[[File:]]"

        self.assertEqual(
            replaceExcept("[[File:x|[[foo]].]]", "x", "y", ["file"], site=self.site), "[[File:x|[[foo]].]]"
        )

        # ensure only links inside file are captured
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]].x]][[x]]", "x", "y", ["file"], site=self.site), "[[File:a|[[foo]].x]][[y]]"
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]][[bar]].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]][[bar]].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]][[bar]].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]][[bar]].x]][[y]]",
        )

        # Correctly handle single brackets in the text.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [bar].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]] [bar].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[bar] [[foo]] .x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[bar] [[foo]] .x]][[y]]",
        )

    def test_replace_tag_file_invalid(self):
        """Test replacing not inside file links with invalid titles."""
        # Correctly handle [ and ] inside wikilinks inside file link
        # even though these are an invalid title.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [invalid] ]].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]] [[bar [invalid] ]].x]][[y]]",
        )

        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [invalid ]].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]] [[bar [invalid ]].x]][[y]]",
        )

    @unittest.expectedFailure
    def test_replace_tag_file_failure(self):
        """Test showing limits of the file link regex."""
        # When the double brackets are unbalanced, the regex
        # does not correctly detect the end of the file link.
        self.assertEqual(
            replaceExcept("[[File:a|[[foo]] [[bar [[invalid ]].x]][[x]]", "x", "y", ["file"], site=self.site),
            "[[File:a|[[foo]] [[bar [invalid] ]].x]][[y]]",
        )

    def test_replace_tags_interwiki(self):
        """Test replacing not inside interwiki links."""
        if "es" not in self.site.family.langs or "ey" in self.site.family.langs:
            raise unittest.SkipTest(f"family {self.site} doesn't have languages")

        self.assertEqual(
            replaceExcept("[[es:s]]", "s", "t", ["interwiki"], site=self.site), "[[es:s]]"
        )  # "es" is a valid interwiki code
        self.assertEqual(
            replaceExcept("[[ex:x]]", "x", "y", ["interwiki"], site=self.site), "[[ey:y]]"
        )  # "ex" is not a valid interwiki code

    def test_replace_template(self):
        """Test replacing not inside templates."""
        template_sample = r"a {{templatename     | accessdate={{Fecha|1993}}     |atitle=The [[real title]] }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"], site=self.site), "X" + template_sample[1:]
        )

        template_sample = r"a {{templatename     | 1={{a}}2{{a}}     | 2={{a}}1{{a}} }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"], site=self.site), "X" + template_sample[1:]
        )

        template_sample = r"a {{templatename     | 1={{{a}}}2{{{a}}}     | 2={{{a}}}1{{{a}}} }}"
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"], site=self.site), "X" + template_sample[1:]
        )

        # sf.net bug 1575: unclosed template
        template_sample = template_sample[:-2]
        self.assertEqual(
            replaceExcept(template_sample, "a", "X", ["template"], site=self.site), "X" + template_sample[1:]
        )

    def test_replace_source_reference(self):
        """Test replacing in text which contains back references."""
        # Don't use a valid reference number in the original string,
        # in case it tries to apply that as a reference.
        self.assertEqual(replaceExcept(r"\42", r"^(.*)$", r"X\1X", [], site=self.site), r"X\42X")
        self.assertEqual(replaceExcept(r"\g<bar>", r"^(?P<foo>.*)$", r"X\g<foo>X", [], site=self.site), r"X\g<bar>X")
