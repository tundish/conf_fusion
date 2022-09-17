#! /usr/bin/env python
# encoding: utf-8

# Copyright (C) 2022 tundish

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

import os
import pathlib
import tempfile
import textwrap
import unittest

from confusion.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        fd, name = tempfile.mkstemp(text=True)
        os.close(fd)
        self.toml_path = pathlib.Path(name)

    def tearDown(self):
        self.toml_path.unlink()

    def test_construct_empty(self):
        rv = Config.from_path(self.toml_path)
        self.assertFalse(rv.tables)

    def test_construct_single_section(self):
        self.toml_path.write_text('[A]\na = "b"')
        rv = Config.from_path(self.toml_path)
        self.assertIn("A", rv.tables)
        self.assertEqual({"a": "b"}, rv.tables["A"])

    def test_merge_missing_section(self):
        text = textwrap.dedent("""
        [A]
        foo = "bar"

        """)
        self.toml_path.write_text(text)

        data = {"B_foo": "baz"}
        rv = Config.from_path(self.toml_path).merge(data)
        self.assertNotIn("B", rv.tables)

    def test_merge_number(self):
        text = textwrap.dedent("""
        [A]
        foo = "bar"

        """)
        self.toml_path.write_text(text)

        data = {"A_foo": 0}
        rv = Config.from_path(self.toml_path).merge(data)
        self.assertEqual(0, rv.tables["A"]["foo"])

    def test_merge_string(self):
        text = textwrap.dedent("""
        [A]
        foo = "bar"

        """)
        self.toml_path.write_text(text)

        data = {"A_foo": "baz"}
        rv = Config.from_path(self.toml_path).merge(data)
        self.assertEqual("baz", rv.tables["A"]["foo"])

    def test_merge_ignores_section_spacing(self):
        text = textwrap.dedent("""
        [ A ]
        foo = "bar"

        """)
        self.toml_path.write_text(text)

        data = {"A_foo": "baz"}
        rv = Config.from_path(self.toml_path).merge(data)
        self.assertEqual("baz", rv.tables["A"]["foo"])

    def test_merge_ignores_section_missing(self):
        text = textwrap.dedent("""
        [ A ]
        foo = "bar"

        """)
        self.toml_path.write_text(text)

        data = {"B_foo": "baz"}
        rv = Config.from_path(self.toml_path).merge(data)
        self.assertEqual("bar", rv.tables["A"]["foo"])
        self.assertNotIn("B", rv.tables)
