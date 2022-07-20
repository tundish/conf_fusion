#! /usr/bin/env python
# encoding: utf-8

import argparse
import configparser
import itertools
import pathlib
import re
import sys


"""
This utility applies configparser substitution patterns as a preprocessor
for, eg: TOML files.

Usage:

    python -m confusion.parser my.ini > my.toml

"""


class FusionParser(configparser.ConfigParser):

    @classmethod
    def loads(cls, text, **kwargs):
        rv = cls(**kwargs)
        rv.read_string(text)
        return rv

    def __init__(self, *args, interpolation=None, **kwargs):
        interpolation = interpolation or configparser.ExtendedInterpolation()
        super().__init__(interpolation=interpolation, **kwargs)
        self.SECTCRE = re.compile("\[\s*(?P<header>\S+)\s*\]")
        self.optionxform = str

    @property
    def sections(self):
        return {k: v for k, v in self.items() if k != self.default_section}

    @property
    def literals(self):
        d = self.defaults()
        return {k: dict(d, **s) for k, s in self.sections.items()}

    def dumps(self):
        rv = [
            itertools.chain(
                (f"[{l}]",),
                (f"{k} = {v}" for k, v in s.items())
            )
            for l, s in self.literals.items()
        ]
        return "\n".join(j for i in rv for j in i)


def main(args):
    if not args.input:
        text = sys.stdin.read()
    else:
        text = args.input.read_text()

    conf = Conf.loads(text)
    print(conf.dumps(), file=sys.stdout)


def parser():
    rv = argparse.ArgumentParser(__doc__)
    rv.add_argument(
        "input", nargs="?", type=pathlib.Path,
        help="Set input file."
    )
    return rv


def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
