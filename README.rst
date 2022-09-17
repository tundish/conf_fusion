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

Let's use this scrap of *CFN* for demonstration::

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

The simplest way to construct a parser is via the *from_string* class method::

    from confusion import Config

    conf = Config.from_string(text)

Or, to read a file, just use the *from_path* method::

    conf = Config.from_path("my_config.cfn")

A Config object has all the methods of Python's standard `ConfigParser class`_.
There is one difference; the *sections* attribute is a property which returns a dictionary::

    print(conf.sections)
    >>> {'A': <Section: A>, 'B': <Section: B>}

The hierarchical TOML data is available via the object's *tables* property::

    print(conf.tables)
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

    conf = Config.from_path("my_config.cfn")
    conf.merge(os.environ)

Only those variables with a corresponding section in the file will be merged in.
You can pass an alternative separator to the `merge` method::

    conf.merge({"window.width": 800, "window.height": 600}, sep=".")

Logging
-------

The Config file has a convenient method to set up your logs according to the `logging configuration schema`_.

This means you can achieve complete configuration of your application in this single line of code::

    conf = Config.from_path("my_config.cfn").merge(os.environ).configure_logging(table_name="logging")

Utilities
=========

``cfn2dot`` is a command line utility which generates a Grapviz *.dot* file from a data graph in confusion format::

    $ python -m confusion.utils.cfn2dot --help

    This utility translates a graph defined in a CFN file to an equivalent .dot

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
.. _configparser class: https://docs.python.org/3/library/configparser.html#configparser.ConfigParser
.. _confusion: https://github.com/tundish/conf_fusion
.. _logging configuration schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
