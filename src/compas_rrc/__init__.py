# isort: skip_file
"""

.. currentmodule:: compas_rrc

Main concepts
=============

The API of ``COMPAS RRC`` is minimal and very easy to understand.

Communication methods
---------------------

The primary way to interact with robots is using the client classes. They allow four
different ways of communication:

* **Send**: The method :meth:`~compas_rrc.AbbClient.send` allows streaming
  commands without blocking or waiting for feedback.
* **Send & Wait**: The method :meth:`~compas_rrc.AbbClient.send_and_wait` sends
  an instruction and wait for feedback from the robot.
* **Send & Wait in the future**: Using the return value of the method
  :meth:`~compas_rrc.AbbClient.send` allows to defer the waiting to a future point in time.
* **Send & Subscribe**: The method :meth:`~compas_rrc.AbbClient.send_and_subscribe` can activate
  a streaming service on the robot that will stream feedback at a regular inverval.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RosClient
    AbbClient
    ExecutionLevel
    FeedbackLevel
    FutureResult

Robot joints and External axes
------------------------------

The following example shows how to retrieve, update and send the robot joints and external axes::

    # Get joints
    robot_joints, external_axes = abb.send_and_wait(rrc.GetJoints())

    # Print received values
    print(robot_joints, external_axes)

    # Change any value and move to new position
    robot_joints.rax_1 += 15
    done = abb.send_and_wait(rrc.MoveToJoints(robot_joints, external_axes, 100, rrc.Zone.FINE))


.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotJoints
    ExternalAxes

Debugging instructions
----------------------

Wrapping any instruction in a :class:`~compas_rrc.Debug` allows to get raw access to the
output values::


    # Get joints
    raw_debug_output = abb.send_and_wait(rrc.Debug(rrc.GetJoints()))

    # Print received values
    print(raw_debug_output)

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Debug

"""

from __future__ import absolute_import

from compas_rrc.__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __license__,
    __url__,
    __version__
)
from compas_rrc.client import (
    AbbClient,
    RosClient
)
from compas_rrc.common import (
    CLIENT_PROTOCOL_VERSION,
    ExecutionLevel,
    ExternalAxes,
    FeedbackLevel,
    FutureResult,
    InstructionException,
    RobotJoints,
    TimeoutException
)
from compas_rrc.custom import CustomInstruction
from compas_rrc.io import (
    PulseDigital,
    ReadAnalog,
    ReadDigital,
    ReadGroup,
    SetAnalog,
    SetDigital,
    SetGroup
)
from compas_rrc.motion import (
    Motion,
    MoveToFrame,
    MoveToJoints,
    MoveToRobtarget,
    Zone
)
from compas_rrc.msg import PrintText
from compas_rrc.utility import (
    Debug,
    GetFrame,
    GetJoints,
    GetRobtarget,
    Noop,
    SetAcceleration,
    SetMaxSpeed,
    SetTool,
    SetWorkObject,
    Stop,
    WaitTime
)
from compas_rrc.watch import (
    ReadWatch,
    StartWatch,
    StopWatch
)

__all_plugins__ = ['compas_rrc.__install']
__all__ = [
    '__url__',
    '__version__',
    '__author__',
    '__author_email__',
    '__license__',
    '__copyright__',
    'CLIENT_PROTOCOL_VERSION',
    'FeedbackLevel',
    'ExecutionLevel',
    'InstructionException',
    'TimeoutException',
    'FutureResult',
    'ExternalAxes',
    'RobotJoints',
    'RosClient',
    'AbbClient',
    'SetDigital',
    'SetAnalog',
    'SetGroup',
    'PulseDigital',
    'ReadAnalog',
    'ReadDigital',
    'ReadGroup',
    'Zone',
    'Motion',
    'MoveToJoints',
    'MoveToFrame',
    'MoveToRobtarget',
    'PrintText',
    'CustomInstruction',
    'Noop',
    'GetFrame',
    'GetJoints',
    'GetRobtarget',
    'SetAcceleration',
    'SetTool',
    'SetMaxSpeed',
    'Stop',
    'WaitTime',
    'SetWorkObject',
    'Debug',
    'ReadWatch',
    'StartWatch',
    'StopWatch',
]
