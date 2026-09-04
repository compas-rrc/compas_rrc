# COMPAS RRC

[![Build Status](https://github.com/compas-rrc/compas_rrc/workflows/build/badge.svg)](https://github.com/compas-rrc/compas_rrc/actions)
[![License](https://img.shields.io/github/license/compas-rrc/compas_rrc.svg)](https://pypi.python.org/pypi/compas_rrc)
[![PyPI Package latest release](https://img.shields.io/pypi/v/compas_rrc.svg)](https://pypi.python.org/pypi/compas_rrc)
[![Conda](https://img.shields.io/conda/vn/conda-forge/compas_rrc.svg)](https://anaconda.org/conda-forge/compas_rrc)
[![Supported implementations](https://img.shields.io/pypi/implementation/compas_rrc.svg)](https://pypi.python.org/pypi/compas_rrc)
[![DOI](https://zenodo.org/badge/296547476.svg)](https://zenodo.org/badge/latestdoi/296547476)
[![Twitter Follow](https://img.shields.io/twitter/follow/compas_dev?style=social)](https://twitter.com/compas_dev)

Online control for ABB robots over a simple-to-use Python interface.

## Main features

* Provides a simple way to interact with ABB robots
* Supports futures and blocking calls
* Works over ROS or MQTT, on top of COMPAS EVE
* Supports all RAPID instructions as well as custom procedures
* Supports EGM activation/deactivation
* Supports multi-move up to 4 robots
* Supports commanding multiple controllers in coordination
* Open up the Python world for ABB robots

**COMPAS RRC** requires Python 3.9 or newer.

## Requirements

`COMPAS RRC` is part of the `COMPAS` framework and it requires the core library
and the event infrastructure package `COMPAS EVE`.

## Installation

First install the pre-requisites in a conda environment:

!!! note

    Make sure to change `ENVIRONMENT_NAME` to a name of your choice

```bash
conda create -c conda-forge -n ENVIRONMENT_NAME compas_rrc python=3.11
conda activate ENVIRONMENT_NAME
```

## Getting started

You can find additional examples to get you started easily on
[the compas_rrc_start repository](https://github.com/compas-rrc/compas_rrc_start).

## Contributing

Check the [Contributor's Guide](https://github.com/compas-rrc/compas_rrc/blob/main/CONTRIBUTING.md).

## Credits

This package was created by Philippe Fleischmann <fleischmann@arch.ethz.ch>
[@fleischp](https://github.com/fleischp) at [@ethrfl](https://github.com/compas-rrc).
