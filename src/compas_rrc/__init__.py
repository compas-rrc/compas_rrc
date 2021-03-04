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

from .client import *  # noqa: F401, F403
from .common import *  # noqa: F401, F403
from .custom import *  # noqa: F401, F403
from .io import *  # noqa: F401, F403
from .motion import *  # noqa: F401, F403
from .msg import *  # noqa: F401, F403
from .utility import *  # noqa: F401, F403
from .watch import *  # noqa: F401, F403

__all__ = [name for name in dir() if not name.startswith('_')]
