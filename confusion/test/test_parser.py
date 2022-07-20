#! /usr/bin/env python
# encoding: utf-8

import unittest

from confusion.parser import FusionParser


class TestParser(unittest.TestCase):

    def test_case(self):
        text = """
        [section]
        A = 1
        """
        conf = FusionParser.loads(text)
        self.assertFalse("a" in conf["section"])

    def test_sections(self):
        text = """
        [A]
        tag = 1

        [A.B.C]
        tag = 1

        [  D ]
        """
        conf = FusionParser.loads(text)
        self.assertEqual(["A", "A.B.C", "D"], list(conf.sections.keys()))

    def test_table(self):
        text = """
        [A]
        tag = 1

        [A.B.C]
        tag = 2

        [  D ]
        """
        conf = FusionParser.loads(text)
        self.assertEqual("1", conf.sections["A"].get("tag"))
        self.assertEqual({"tag": "2"}, dict(conf.sections["A.B.C"]))

    def test_get(self):
        text = """
        [A.B.C]
        tag = 1
        """
        conf = FusionParser.loads(text)
        self.assertEqual({"tag": "1"}, dict(conf.sections["A.B.C"]))

    def test_defaults(self):
        text = """
        [DEFAULT]
        flavour = vanilla
        [A]
        [B]
        flavour = strawberry
        """
        conf = FusionParser.loads(text)
        self.assertEqual("vanilla", conf.sections["A"].get("flavour"))
        self.assertEqual("strawberry", conf.sections["B"].get("flavour"))

    def test_substitution(self):
        text = """
        [DEFAULT]
        flavour = vanilla
        [A]
        flavour = strawberry
        [B]
        flavour = ${A:flavour}
        """
        conf = FusionParser.loads(text)
        self.assertEqual("strawberry", conf.sections["A"].get("flavour"))
        self.assertEqual("strawberry", conf.sections["B"].get("flavour"))

    def test_loads(self):
        text = """
        [A]
        [B]
        """
        conf = FusionParser.loads(text)
        self.assertIsInstance(conf, FusionParser)

    def test_literals(self):
        text = """
        [DEFAULT]
        flavour = vanilla
        [A]
        flavour = strawberry
        [B]
        flavour = ${A:flavour}
        """
        conf = FusionParser.loads(text)

    def test_dumps_simple(self):
        text = """
        [A]
        [B]
        """
        conf = FusionParser.loads(text)
        rv = conf.dumps()
        self.assertEqual("[A]\n[B]", rv)

    def test_dumps_substitution(self):
        text = """
        [DEFAULT]
        flavour = vanilla
        [A]
        flavour = strawberry
        [B]
        flavour = ${A:flavour}
        """
        conf = FusionParser.loads(text)
        rv = conf.dumps()
        self.assertNotIn("$", rv)

    def test_dumps_quotes(self):
        text = """
        [A]
        label = "day/night cycles"
        [B]
        color = {"r" = 0, "g" = 0, "b" = 0}
        """
        conf = FusionParser.loads(text)
        rv = conf.dumps()
        self.assertEqual(8, rv.count('"'))
