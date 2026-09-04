# COMPAS RRC

![COMPAS RRC](_images/compas_rrc.png)

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

Then head over to [Getting started](getting_started.md).
