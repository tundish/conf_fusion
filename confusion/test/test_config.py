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
