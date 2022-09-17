Confusion
+++++++++

This package defines a *Config* class which allows you to employ an extended syntax in your TOML files.

Syntax
======

Defaults
--------

Consider this scrap of TOML::

    [A]

    [B]
    flavour = "strawberry"

Confusion_ lets you add a `DEFAULT` section just like the traditional Python `configparser module`_::

    [DEFAULT]
    flavour = "vanilla"

    [A]

    [B]
    flavour = "strawberry"

Substitution
------------

By applying the extended substitution syntax, you can define a value in only one location and reference
it elsewhere (DRY principle)::

    [A]
    flavour = "strawberry"

    [B]
    flavour = ${A:flavour}

Cross-compatible strings
------------------------

Multiline strings have to be formatted to conform to both *configparser* and *TOML* syntaxes::

    [caveat]
    text = """
        Multiline strings
        are possible but
        indentation of these closing quotes
        is required.
        """

Usage
=====

Let's use this scrap of TOML for demonstration::

    text = """

    [DEFAULT]
    flavour = "vanilla"
    flake = false

    [A]
    flavour = "strawberry"

    [B]
    flavour = ${A:flavour}
    flake = true

    """

The simplest way to construct a parser is using the *from_string* class method::

    from confusion import Config

    parser = Config.from_string(text)

To create a Config object from a file, just use the `from_path` method::

    parser = Config.from_path("my_config.cfn")

A Config object has all the methods of Python's standard `ConfigParser`.
There is one difference; the *sections* attribute is a property which returns a dictionary::

    print(parser.sections)
    >>> {'A': <Section: A>, 'B': <Section: B>}

The hierarchical TOML data is available via the object's *tables* property::

    print(parser.tables)
    >>> {'A': {'flavour': 'strawberry', 'flake': False}, 'B': {'flavour': 'strawberry', 'flake': True}}

Environment variables
---------------------

You can override settings in the Config object from a flat dictionary.
Keys in the dictionary are parsed for a separator ('_' by default) which denotes the section
in which the setting belongs.

Suppose you want to avoid storing a password in this file::

    [DB]
    USER = "postgres"

You can define an environment variable *DB_PASS=postgres* and merge it in from there::

    import os

    parser = Config.from_path("connection.cfn")
    parser.merge(os.environ)

Only those variables with a corresponding section in the file will be merged in.
You can pass an alternative separator to the `merge` method::

    parser.merge({"window.width": 800, "window.height": 600}, sep=".")

Utilities
=========

*TOML2dot* is a command line utility which generates a Grapviz *.dot* file from a data graph in confusion format::

    $ python -m confusion.utils.cfn2dot --help

    This utility translates a graph defined in a TOML file to an equivalent .dot

    Usage:

        python -m confusion.utils.cfn2dot --label-graph Taxonomy --digraph taxonomy.cfn > taxonomy.dot

        dot -Tsvg taxonomy.dot > taxonomy.svg

           [-h] [--label-graph LABEL_GRAPH] [--label-inherits LABEL_INHERITS] [--cluster] [--digraph] input [input ...]

    positional arguments:
      input                 Set input file.

    options:
      -h, --help            show this help message and exit
      --label-graph LABEL_GRAPH
                            Set a label for the graph.
      --label-inherits LABEL_INHERITS
                            Set the label for an arc signifying an 'inherits' relationship.
      --cluster             Generate a clustered graph.
      --digraph, --directed
                            Make arcs directional.

.. _configparser module: https://docs.python.org/3/library/configparser.html#module-configparser
.. _confusion: https://github.com/tundish/conf_fusion
