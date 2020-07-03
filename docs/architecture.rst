Software Architecture
=====================

This document describes the architecture of COMPAS RRC, and documents
design decisions taken during development.

Protocol Specification
----------------------

The protocol specification is located in ``YYMMDD_A042_Protokoll_PF.xlsx``.

Protocol Version check
----------------------

The following procedure is used to verify the protocol versions between ``Python RRC Client``,
``ROS Driver`` and ``RRC Server`` are all matching:

* ``Python RRC Client`` <-> ``ROS Driver``:
    * On start, ROS Driver sets current procol version into a parameter.
    * On connect, Python RRC Client checks protocol version in parameter matches its own protocol version and raises an exception **if not the same**.
* ``ROS Driver`` -> ``RRC Server``
    * ROS Driver sends current procol version on every message (as defined in the protocol specification).
    * RRC Server checks first protocol after ``PP to Main`` and stops with a message **if not the same**.
* ``RRC Server`` -> ``ROS Driver``
   * Every feedback from the robot contains protocol version in the header.
   * ROS Driver checks protocol version on first feedback after the connection, and raises an exception **if not the same**.
