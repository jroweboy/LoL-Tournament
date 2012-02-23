"""Tests to ensure that the lxml tree builder generates good trees."""

import re

try:
    from bs4.builder import LXMLTreeBuilder, LXMLTreeBuilderForXML
    LXML_PRESENT = True
except ImportError, e:
    LXML_PRESENT = False

from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype, SoupStrainer
from bs4.testing import skipIf
from bs4.tests import test_htmlparser
from bs4.testing import (
    HTMLTreeBuilderSmokeTest,
    SoupTest,
    skipIf,
)

@skipIf(
    not LXML_PRESENT,
    "lxml seems not to be present, not testing its tree builder.")
class LXMLTreeBuilderSmokeTest(SoupTest, HTMLTreeBuilderSmokeTest):
    """See ``HTMLTreeBuilderSmokeTest``."""

    @property
    def default_builder(self):
        return LXMLTreeBuilder()

    def test_out_of_range_entity(self):
        self.assertSoupEquals(
            "<p>foo&#10000000000000;bar</p>", "<p>foobar</p>")
        self.assertSoupEquals(
            "<p>foo&#x10000000000000;bar</p>", "<p>foobar</p>")
        self.assertSoupEquals(
            "<p>foo&#1000000000;bar</p>", "<p>foobar</p>")
