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

Software Architecture Layers
----------------------------

RRC is composed by three layers:

* User-level: the ``Python RRC Client``, a simple-to-use Python interface which can be used as a library on any python application and/or script.
* Middleware-level: the ``ROS Driver`` running as a ROS package which acts as intermediary between robot code and user code.
* Robot-level: the ``RRC Server`` running as an application on the robot controller and the system interface (eg. ``Robot Web Service`` in the case of ABB robots).

Interfaces
----------

There are two interfaces supported by RRC:

* ``System``: The system interface connects to system-level services on the robot.
* ``Application``: The application interface connects to the robot application via TCP using the RRC protocol specified above.

Data Parsing/Conversion
-----------------------

There are three different data type representations involved in the process of sending and receiving data:

* Python data types (eg. ``compas.geometry.Frame``)
* JSON/stringified representation of data types
* Robot data types (eg. ``tooldata`` for ABB RAPID)

Rules:

* ``Python RRC Client`` is the only layer that converts from/to high-level data types, such as ``compas.geometry.Frame``.
* ``ROS Driver`` only knows about Python built-in data types and the conversions required to/from the RRC protocol, which includes the conversion of Python built-in data types to Robot-native data types.
* ``RRC Server`` only knows about the RRC protocol and how to convert to native actions.
* ``ROS Driver`` does not have a dependency to COMPAS library.


Example Workflows
-----------------

* Move to Frame using Application interface:
    * ``Python RRC Client`` input is ``MoveToFrame(frame)`` -> converts to strings/floats values according to the protocol -> converted to JSON for topic publishing ->
    * ``ROS Driver`` input is topic message -> converts from strings/floats values to bytes of the wire protocol -> sends over TCP/IP
    * ``RRC Server`` input is TCP/IP message -> converts to RAPID actions -> creates feedback and sends it over TCP/IP
    * ``ROS Driver`` input is TCP/IP message -> convert to JSON for topic publishing ->
    * ``Python RRC Client`` input is topic message -> convert to feedback string (``Done``)

* Get Frame using Application interface:
    * ``Python RRC Client`` input is ``GetFrame()`` -> converts to strings/floats values according to the protocol -> converted to JSON for topic publishing ->
    * ``ROS Driver`` input is topic message -> converts from strings/floats values to bytes of the wire protocol -> sends over TCP/IP
    * ``RRC Server`` input is TCP/IP message -> converts to RAPID actions -> creates feedback and sends it over TCP/IP
    * ``ROS Driver`` input is TCP/IP message -> converts to Python built-in data types -> convert to JSON for topic publishing
    * ``Python RRC Client`` input is topic message -> converts from JSON to ``compas.geometry.Frame``.

* Get Variable using System interface:
    * ``Python RRC Client`` input is ``GetVariable(name)`` -> converts to strings/floats values according to the protocol -> converted to JSON for topic publishing ->
    * ``ROS Driver`` input is topic message -> converts from strings/floats values to REST JSON request -> sends request to system interface ``Robot Web Service``
    * ``Robot Web Service`` input is REST JSON request -> returns REST JSON response
    * ``ROS Driver`` input is REST JSON response -> parse RAPID string to Python built-in data types (using ``ply``) -> convert Python built-in data types (including complex dictionaries if needed) to JSON for topic publishing (``string_values[0]`` is the JSON string serialization of the variable value) ->
    * ``Python RRC Client`` input is topic message -> loads variable value in JSON from ``string_values[0]`` and converts from Python built-in data types to COMPAS and other complex data types, eg. ``compas.geometry.Frame``.

* Set Variable using System interface:
    * ``Python RRC Client`` input is ``SetVariable(name, value)`` -> converts to strings/floats values according to the protocol (``string_value[0]`` is variable name, ``string_value[1]`` is data representation of variable as JSON string) -> converted to JSON for topic publishing ->
    * ``ROS Driver`` input is topic message -> converts from strings/floats values to REST JSON request including the conversion of ``string_value[1]`` JSON string to a Robot-native data type -> sends request to system interface ``Robot Web Service``
    * ``Robot Web Service`` input is REST JSON request -> returns REST JSON response
    * ``ROS Driver`` input is REST JSON response -> convert to JSON for topic publishing ->
    * ``Python RRC Client`` input is topic message -> convert to feedback string (``Done``)
