==========
COMPAS RRC
==========

Library of instructions for ABB Robots using COMPAS RRC Driver.

Main features
-------------

* Provides a simple way to interact with ABB robots
* Supports futures and blocking calls
* Builds on top of COMPAS FAB.

**COMPAS RRC** runs on Python 3.x as well as IronPython 2.7.

Requirements
------------

``COMPAS RRC`` is part of the ``COMPAS`` framework and it requires
the core library and the robotic fabrication package ``COMPAS FAB``.


Installation
------------

First install the pre-requisites in a conda environment:

.. note::

    Make sure to change ``ENVIRONMENT_NAME`` to a name of your choice

::

    conda create -c conda-forge -n ENVIRONMENT_NAME compas_fab python=3.8
    conda activate ENVIRONMENT_NAME

And then install ``COMPAS RRC``:

::

    pip install git+https://@github.com/compas-rrc/compas_rrc.git


Contributing
------------

Make sure you setup your local development environment correctly:

* Clone the `compas_rrc <https://github.com/compas-rrc/compas_rrc>`_ repository.
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
* ``invoke``: Show available tasks.

For more details, check the `Contributor's Guide <CONTRIBUTING.rst>`_.

Credits
-------------

This package was created by Philippe Fleischmann <fleischmann@arch.ethz.ch> `@fleischp <https://github.com/fleischp>`_ at `@ethrfl <https://github.com/compas-rrc>`_
