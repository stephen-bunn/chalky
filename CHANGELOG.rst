=========
Changelog
=========

| All notable changes to this project will be documented in this file.
| The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.
|

.. towncrier release notes start

`0.3.0 <https://github.com/stephen-bunn/chalky/releases/tag/v0.3.0>`_ (*2020-12-25*)
====================================================================================

Features
--------

- Including a global :func:`~.constants.configure` callable to handle configuring the
  entire module.
  At the moment, the only feature we are adding is the ability to completely disable the
  actual application of styles and colors through the ``disable`` flag.

Documentation
-------------

- Adding some simple chalky chaining documentation.


`0.2.0 <https://github.com/stephen-bunn/chalky/releases/tag/v0.2.0>`_ (*2020-12-24*)
====================================================================================

Features
--------

- | Adding an interface for producing styles and colors using chained properties.
  | Usage looks like this:

   .. code-block:: python
      :linenos:

      from chalky import chain
      print(chain.bold.blue | "I'm blue bold text!")

Documentation
-------------

- Adding some chaining documentation.
- Adding basic usage documentation for the initial release.

Miscellaneous
-------------

- Adding a basic Chalky logo to make the documentation a bit more friendly.


`0.1.0 <https://github.com/stephen-bunn/chalky/releases/tag/v0.1.0>`_ (*2020-12-23*)
====================================================================================

Miscellaneous
-------------

- Adding the contents of an initial alpha release.
