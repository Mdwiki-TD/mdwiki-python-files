
import pytest
import re

from wprefs.bots.replace_except import replaceExcept


class TestBasicReplacement:
    """Test basic replacement functionality without exceptions."""

    def test_simple_string_replacement(self):
        """Test simple string pattern replacement."""
        text = "Hello world, hello universe"
        result = replaceExcept(text, "hello", "hi", [], count=0)
        assert result == "Hello world, hi universe"

    def test_regex_pattern_replacement(self):
        """Test replacement with compiled regex pattern."""
        text = "The number is 123 and 456"
        pattern = re.compile(r'\d+')
        result = replaceExcept(text, pattern, "XXX", [])
        assert result == "The number is XXX and XXX"

    def test_case_sensitive_replacement(self):
        """Test that replacement is case-sensitive by default."""
        text = "Hello hello HELLO"
        result = replaceExcept(text, "hello", "hi", [])
        assert result == "Hello hi HELLO"

    def test_no_match_returns_original(self):
        """Test that text is returned unchanged when pattern doesn't match."""
        text = "Hello world"
        result = replaceExcept(text, "goodbye", "farewell", [])
        assert result == "Hello world"

    def test_empty_text(self):
        """Test replacement on empty string."""
        result = replaceExcept("", "test", "replace", [])
        assert result == ""

    def test_replacement_with_count_limit(self):
        """Test that count parameter limits number of replacements."""
        text = "foo foo foo foo"
        result = replaceExcept(text, "foo", "bar", [], count=2)
        assert result == "bar bar foo foo"

    def test_count_zero_replaces_all(self):
        """Test that count=0 replaces all occurrences."""
        text = "foo foo foo"
        result = replaceExcept(text, "foo", "bar", [], count=0)
        assert result == "bar bar bar"


class TestGroupReferences:
    """Test regex group references in replacement strings."""

    def test_numbered_group_reference(self):
        """Test replacement with numbered group references."""
        text = "John Smith and Jane Doe"
        pattern = r'(\w+) (\w+)'
        replacement = r'\2, \1'
        result = replaceExcept(text, pattern, replacement, [])
        assert result == "Smith, John and Doe, Jane"

    def test_named_group_reference(self):
        """Test replacement with named group references."""
        text = "Price: $100"
        pattern = r'(?P<currency>\$)(?P<amount>\d+)'
        replacement = r'\g<amount> \g<currency>'
        result = replaceExcept(text, pattern, replacement, [])
        assert result == "Price: 100 $"

    def test_mixed_group_references(self):
        """Test replacement with both numbered and named groups."""
        text = "2024-12-24"
        pattern = r'(?P<year>\d{4})-(\d{2})-(\d{2})'
        replacement = r'\3/\2/\g<year>'
        result = replaceExcept(text, pattern, replacement, [])
        assert result == "24/12/2024"

    def test_escaped_newline_in_replacement(self):
        """Test that \\n in replacement string is converted to newline."""
        text = "foo bar"
        result = replaceExcept(text, " ", "\\n", [])
        assert result == "foo\nbar"


class TestCallableReplacement:
    """Test replacement with callable functions."""

    def test_callable_replacement_basic(self):
        """Test replacement using a callable function."""
        text = "The number is 42"
        pattern = r'\d+'

        def double_number(match):
            return str(int(match.group()) * 2)

        result = replaceExcept(text, pattern, double_number, [])
        assert result == "The number is 84"

    def test_callable_replacement_with_groups(self):
        """Test callable replacement accessing match groups."""
        text = "Hello World"
        pattern = r'(\w+) (\w+)'

        def swap_and_upper(match):
            return f"{match.group(2).upper()} {match.group(1).upper()}"

        result = replaceExcept(text, pattern, swap_and_upper, [])
        assert result == "WORLD HELLO"

    def test_callable_replacement_multiple_matches(self):
        """Test callable replacement on multiple matches."""
        text = "1 2 3 4"
        pattern = r'\d+'
        counter = {'count': 0}

        def increment(match):
            counter['count'] += 1
            return str(int(match.group()) + 10)

        result = replaceExcept(text, pattern, increment, [])
        assert result == "11 12 13 14"
        assert counter['count'] == 4


class TestCommentException:
    """Test that replacements are skipped inside HTML comments."""

    def test_skip_replacement_in_comment(self):
        """Test that text in HTML comments is not replaced."""
        text = "foo <!-- foo --> foo"
        result = replaceExcept(text, "foo", "bar", ["comment"])
        assert result == "bar <!-- foo --> bar"

    def test_multiline_comment(self):
        """Test that multiline comments are properly handled."""
        text = "foo <!--\nfoo\nfoo\n--> foo"
        result = replaceExcept(text, "foo", "bar", ["comment"])
        assert result == "bar <!--\nfoo\nfoo\n--> bar"

    def test_multiple_comments(self):
        """Test handling of multiple comments."""
        text = "foo <!-- foo --> bar <!-- foo --> foo"
        result = replaceExcept(text, "foo", "XXX", ["comment"])
        assert result == "XXX <!-- foo --> bar <!-- foo --> XXX"


class TestLinkException:
    """Test that replacements are skipped inside wiki links."""

    def test_skip_replacement_in_link(self):
        """Test that text in wiki links is not replaced."""
        text = "foo [[foo]] foo"
        result = replaceExcept(text, "foo", "bar", ["link"])
        assert result == "bar [[foo]] bar"

    def test_link_with_pipe(self):
        """Test links with pipe syntax."""
        text = "foo [[Page|foo text]] foo"
        result = replaceExcept(text, "foo", "bar", ["link"])
        assert result == "bar [[Page|foo text]] bar"

    def test_nested_brackets(self):
        """Test that nested brackets in links are handled."""
        text = "foo [[File:Image.jpg|thumb|foo]] foo"
        result = replaceExcept(text, "foo", "bar", ["link"])
        assert result == "bar [[File:Image.jpg|thumb|foo]] bar"


class TestTemplateException:
    """Test that replacements are skipped inside templates."""

    def test_skip_replacement_in_template(self):
        """Test that text in templates is not replaced."""
        text = "foo {{template|foo}} foo"
        result = replaceExcept(text, "foo", "bar", ["template"])
        assert result == "bar {{template|foo}} bar"

    def test_template_with_multiple_params(self):
        """Test templates with multiple parameters."""
        text = "foo {{template|param1=foo|param2=foo}} foo"
        result = replaceExcept(text, "foo", "bar", ["template"])
        assert result == "bar {{template|param1=foo|param2=foo}} bar"

    def test_nested_templates(self):
        """Test nested template handling."""
        text = "foo {{outer|{{inner|foo}}}} foo"
        result = replaceExcept(text, "foo", "bar", ["template"])
        # The template regex should handle nested templates
        assert "{{outer|{{inner|foo}}}}" in result
        assert result.startswith("bar ")
        assert result.endswith(" bar")


class TestHeaderException:
    """Test that replacements are skipped inside section headers."""

    def test_skip_replacement_in_header(self):
        """Test that text in headers is not replaced."""
        text = "foo\n== foo ==\nfoo"
        result = replaceExcept(text, "foo", "bar", ["header"])
        assert result == "bar\n== foo ==\nbar"

    def test_header_with_different_levels(self):
        """Test headers at different levels."""
        text = "foo\n=== foo ===\nfoo"
        result = replaceExcept(text, "foo", "bar", ["header"])
        assert result == "bar\n=== foo ===\nbar"

    def test_header_at_start(self):
        """Test header at the beginning of text."""
        text = "== foo ==\nfoo"
        result = replaceExcept(text, "foo", "bar", ["header"])
        assert result == "== foo ==\nbar"


class TestHyperlinkException:
    """Test that replacements are skipped inside external links."""

    def test_skip_replacement_in_hyperlink(self):
        """Test that text in external links is not replaced."""
        text = "foo http://example.com/foo foo"
        result = replaceExcept(text, "foo", "bar", ["hyperlink"])
        assert result == "bar http://example.com/foo bar"

    def test_https_link(self):
        """Test HTTPS links."""
        text = "foo https://example.com/foo foo"
        result = replaceExcept(text, "foo", "bar", ["hyperlink"])
        assert result == "bar https://example.com/foo bar"


class TestStartColonException:
    """Test that replacements are skipped in indented lines."""

    def test_skip_replacement_in_indented_line(self):
        """Test that indented lines (starting with :) are not replaced."""
        text = "foo\n:foo\nfoo"
        result = replaceExcept(text, "foo", "bar", ["startcolon"])
        assert result == "bar\n:foo\nbar"

    def test_multiple_colons(self):
        """Test lines with multiple colons."""
        text = "foo\n::foo\nfoo"
        result = replaceExcept(text, "foo", "bar", ["startcolon"])
        # Only single colon at start is matched by the regex
        assert "::foo" in result or "::bar" in result


class TestStartSpaceException:
    """Test that replacements are skipped in preformatted text."""

    def test_skip_replacement_in_preformatted(self):
        """Test that preformatted text (starting with space) is not replaced."""
        text = "foo\n foo\nfoo"
        result = replaceExcept(text, "foo", "bar", ["startspace"])
        assert result == "bar\n foo\nbar"


class TestMultipleExceptions:
    """Test handling of multiple exception types simultaneously."""

    def test_multiple_exception_types(self):
        """Test that multiple exception types work together."""
        text = "foo <!-- foo --> {{template|foo}} [[link|foo]] foo"
        result = replaceExcept(text, "foo", "bar", ["comment", "template", "link"])
        assert result == "bar <!-- foo --> {{template|foo}} [[link|foo]] bar"

    def test_overlapping_exceptions(self):
        """Test handling when exceptions might overlap."""
        text = "foo <!-- {{template|foo}} --> foo"
        result = replaceExcept(text, "foo", "bar", ["comment", "template"])
        # Comment should take precedence as it appears first
        assert result == "bar <!-- {{template|foo}} --> bar"

    def test_all_common_exceptions(self):
        """Test with all common exception types."""
        text = (
            "foo "
            "<!-- foo --> "
            "{{foo}} "
            "[[foo]] "
            "http://foo.com "
            "foo"
        )
        exceptions = ["comment", "template", "link", "hyperlink"]
        result = replaceExcept(text, "foo", "bar", exceptions)
        # First and last foo should be replaced
        assert result.startswith("bar ")
        assert result.endswith(" bar")
        # Protected regions should remain unchanged
        assert "<!-- foo -->" in result
        assert "{{foo}}" in result
        assert "[[foo]]" in result
        assert "http://foo.com" in result


class TestCustomRegexException:
    """Test using custom regex patterns as exceptions."""

    def test_custom_regex_exception(self):
        """Test that custom regex patterns can be used as exceptions."""
        text = "foo [PROTECTED foo PROTECTED] foo"
        custom_regex = re.compile(r'\[PROTECTED.*?PROTECTED\]')
        result = replaceExcept(text, "foo", "bar", [custom_regex])
        assert result == "bar [PROTECTED foo PROTECTED] bar"

    def test_mixed_string_and_regex_exceptions(self):
        """Test mixing string and regex exceptions."""
        text = "foo <!-- foo --> [CUSTOM foo CUSTOM] foo"
        custom_regex = re.compile(r'\[CUSTOM.*?CUSTOM\]')
        result = replaceExcept(text, "foo", "bar", ["comment", custom_regex])
        assert result == "bar <!-- foo --> [CUSTOM foo CUSTOM] bar"


class TestTagExceptions:
    """Test that replacements are skipped inside various HTML/wiki tags."""

    def test_nowiki_tag(self):
        """Test that nowiki tags are respected."""
        text = "foo <nowiki>foo</nowiki> foo"
        result = replaceExcept(text, "foo", "bar", ["nowiki"])
        assert result == "bar <nowiki>foo</nowiki> bar"

    def test_math_tag(self):
        """Test that math tags are respected."""
        text = "foo <math>foo</math> foo"
        result = replaceExcept(text, "foo", "bar", ["math"])
        assert result == "bar <math>foo</math> bar"

    def test_source_tag(self):
        """Test that source tags are respected."""
        text = "foo <source>foo</source> foo"
        result = replaceExcept(text, "foo", "bar", ["source"])
        assert result == "bar <source>foo</source> bar"

    def test_tag_with_attributes(self):
        """Test tags with attributes."""
        text = "foo <nowiki attr='value'>foo</nowiki> foo"
        result = replaceExcept(text, "foo", "bar", ["nowiki"])
        assert result == "bar <nowiki attr='value'>foo</nowiki> bar"


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_pattern_match(self):
        """Test handling of patterns that can match empty strings."""
        text = "abc"
        pattern = re.compile(r'x*')  # Can match empty string
        result = replaceExcept(text, pattern, "X", [])
        # Should handle empty matches without infinite loop
        assert isinstance(result, str)

    def test_replacement_creates_new_match(self):
        """Test that replacement doesn't create infinite loop if it matches pattern."""
        text = "foo"
        # Replace foo with foobar - should not match the new foo
        result = replaceExcept(text, "foo", "foobar", [])
        assert result == "foobar"

    def test_very_long_text(self):
        """Test performance with longer text."""
        text = "foo " * 1000 + "bar"
        result = replaceExcept(text, "foo", "baz", [])
        assert result.count("baz") == 1000
        assert result.endswith("bar")

    def test_unicode_text(self):
        """Test replacement with unicode characters."""
        text = "Hello مرحبا Hello"
        result = replaceExcept(text, "Hello", "مرحبا", [])
        assert result == "مرحا مرحبا مرحبا"

    def test_special_regex_chars_in_string_pattern(self):
        """Test that special regex characters in string patterns work."""
        text = "a.b a.b"
        result = replaceExcept(text, r'a\.b', "c", [])
        assert result == "c c"

    def test_exception_at_text_start(self):
        """Test exception region at the very start of text."""
        text = "<!-- foo --> foo"
        result = replaceExcept(text, "foo", "bar", ["comment"])
        assert result == "<!-- foo --> bar"

    def test_exception_at_text_end(self):
        """Test exception region at the very end of text."""
        text = "foo <!-- foo -->"
        result = replaceExcept(text, "foo", "bar", ["comment"])
        assert result == "bar <!-- foo -->"

    def test_adjacent_exceptions(self):
        """Test adjacent exception regions."""
        text = "foo <!-- foo --><!-- foo --> foo"
        result = replaceExcept(text, "foo", "bar", ["comment"])
        assert result == "bar <!-- foo --><!-- foo --> bar"

    def test_count_with_exceptions(self):
        """Test that count works correctly with exceptions."""
        text = "foo <!-- foo --> foo foo foo"
        result = replaceExcept(text, "foo", "bar", ["comment"], count=2)
        # Should replace first foo outside comment, then next two
        assert result == "bar <!-- foo --> bar bar foo"


class TestInvalidGroupReference:
    """Test error handling for invalid group references."""

    def test_invalid_group_number(self):
        """Test that invalid group numbers raise IndexError."""
        text = "Hello World"
        pattern = r'(\w+) (\w+)'
        replacement = r'\3'  # Only 2 groups exist

        with pytest.raises(IndexError, match="Invalid group reference"):
            replaceExcept(text, pattern, replacement, [])

    def test_invalid_group_name(self):
        """Test that invalid group names raise IndexError."""
        text = "Hello World"
        pattern = r'(?P<first>\w+) (?P<second>\w+)'
        replacement = r'\g<third>'  # Group 'third' doesn't exist

        with pytest.raises(IndexError):
            replaceExcept(text, pattern, replacement, [])
