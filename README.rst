Confusion
=========

This little package allows you to use default attributes and variable substitution in your TOML files.

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


.. _configparser module: https://docs.python.org/3/library/configparser.html#module-configparser
.. _confusion: https://github.com/tundish/conf_fusion
