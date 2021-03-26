==========
COMPAS RRC
==========

.. start-badges

.. image:: https://github.com/compas-rrc/compas_rrc/workflows/build/badge.svg
    :target: https://github.com/compas-rrc/compas_rrc/actions
    :alt: Github Actions Build Status

.. image:: https://img.shields.io/github/license/compas-rrc/compas_rrc.svg
    :target: https://pypi.python.org/pypi/compas_rrc
    :alt: License

.. image:: https://img.shields.io/pypi/v/compas_rrc.svg
    :target: https://pypi.python.org/pypi/compas_rrc
    :alt: PyPI Package latest release

.. image:: https://img.shields.io/conda/vn/conda-forge/compas_rrc.svg
    :target: https://anaconda.org/conda-forge/compas_rrc

.. image:: https://img.shields.io/pypi/implementation/compas_rrc.svg
    :target: https://pypi.python.org/pypi/compas_rrc
    :alt: Supported implementations

.. image:: https://img.shields.io/twitter/follow/compas_dev?style=social
   :target: https://twitter.com/compas_dev
   :alt: Twitter Follow

.. end-badges

Online control for ABB robots over a simple-to-use Python interface.

Main features
-------------

* Provides a simple way to interact with ABB robots
* Supports futures and blocking calls
* Builds on top of COMPAS FAB
* Supports all RAPID instructions as well as custom procedures
* Supports EGM activation/deactivation
* Supports multi-move up to 4 robots
* Supports commanding multiple controllers in coordination
* Open up the Python world for ABB robots

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

    conda create -c conda-forge -n ENVIRONMENT_NAME compas_rrc python=3.8
    conda activate ENVIRONMENT_NAME


Getting started
---------------

You can find additional examples to get your started easily on `the compas_rrc_start repository <https://github.com/compas-rrc/compas_rrc_start>`_.

Contributing
------------

Check the `Contributor's Guide <https://github.com/compas-rrc/compas_rrc/blob/main/CONTRIBUTING.rst>`_.

Credits
-------------

This package was created by Philippe Fleischmann <fleischmann@arch.ethz.ch> `@fleischp <https://github.com/fleischp>`_ at `@ethrfl <https://github.com/compas-rrc>`_
