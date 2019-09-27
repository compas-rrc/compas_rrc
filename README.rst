==========
COMPAS RRC
==========

.. start-badges

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://bitbucket.org/ethrfl/compas_rrc/blob/master/LICENSE
    :alt: License MIT

.. image:: https://travis-ci.org/ethrfl/compas_rrc.svg?branch=master
    :target: https://travis-ci.org/ethrfl/compas_rrc
    :alt: Travis CI

.. end-badges

Library of instructions for ABB Robots using COMPAS RRC Driver.

Main features
-------------

* Provides a simple way to interact with ABB robots
* Supports futures and blocking calls
* Builds on top of COMPAS FAB.

**COMPAS RRC** runs on Python x.x and x.x.

Requirements
------------

``COMPAS RRC`` is part of the ``COMPAS`` framework and it requires
the core library and the robotic fabrication package ``COMPAS FAB``.


Installation
------------

.. Write installation instructions here


Contributing
------------

Make sure you setup your local development environment correctly:

* Clone the `compas_rrc <https://bitbucket.org/ethrfl/compas_rrc>`_ repository.
* Install development dependencies and make the project accessible from Rhino:

::

    pip install -r requirements-dev.txt
    invoke add-to-rhino

**You're ready to start working!**

During development, use tasks on the
command line to ease recurring operations:

* ``invoke clean``: Clean all generated artifacts.
* ``invoke check``: Run various code and documentation style checks.
* ``invoke docs``: Generate documentation.
* ``invoke test``: Run all tests and checks in one swift command.
* ``invoke add-to-rhino``: Make the project accessible from Rhino.
* ``invoke``: Show available tasks.

For more details, check the `Contributor's Guide <CONTRIBUTING.rst>`_.


Releasing this project
----------------------

.. Write releasing instructions here


.. end of optional sections
..

Credits
-------------

This package was created by Philippe Fleischmann <fleischmann@arch.ethz.ch> `@fleischp <https://github.com/fleischp>`_ at `@ethrfl <https://bitbucket.org/ethrfl>`_
