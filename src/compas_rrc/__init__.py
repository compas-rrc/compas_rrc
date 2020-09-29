"""

The API of ``COMPAS RRC`` is minimal and very easy to understand.

ABB Client
===================

This is the primary way to interact with robots. It contains two
methods that are used for almost all communication:

 * ``send``: Sends a command without waiting for feedback.
 * ``send_and_wait``: Sends a command and waits for the robot
   to respond before continuing to the next line of code.

.. autoclass:: AbbClient
   :members:
.. autoclass:: ExecutionLevel
   :members:
   :undoc-members:
   :member-order: bysource

Handling feedback
-----------------

For cases in which you wish to send a command and wait for feedback, the
easiest option is to use ``send_and_wait``, but for fine-grained control of
when to wait for feedback, the ``send`` methods returns an object of type
:class:`FutureResult`. The call is non-blocking, so it returns immediatelly
but when the ``result()`` method of the future result is invoked, it will block
until the result is eventually available.

.. autoclass:: FeedbackLevel
   :members:
   :undoc-members:
   :member-order: bysource
.. autoclass:: FutureResult
   :members:

Robot joints and External axes
==============================

.. autoclass:: RobotJoints
   :members:
   :undoc-members:
   :member-order: bysource
.. autoclass:: ExternalAxes
   :members:
   :undoc-members:
   :member-order: bysource

Motion instructions
===================

.. autoclass:: MoveToJoints
   :members:
.. autoclass:: MoveToFrame
   :members:
.. autoclass:: MoveToRobtarget
   :members:
.. autoclass:: Motion
   :members:
   :undoc-members:
   :member-order: bysource
.. autoclass:: Zone
   :members:
   :undoc-members:
   :member-order: bysource

Get Current Status
==================

.. autoclass:: GetFrame
   :members:
.. autoclass:: GetJoints
   :members:
.. autoclass:: GetRobtarget
   :members:

Input/Output
============

.. autoclass:: ReadAnalog
   :members:
.. autoclass:: ReadDigital
   :members:
.. autoclass:: ReadGroup
   :members:
.. autoclass:: SetAnalog
   :members:
.. autoclass:: SetDigital
   :members:
.. autoclass:: SetGroup
   :members:
.. autoclass:: PulseDigital
   :members:

Custom instructions
===================

This library has support for non-standard instructions. Simply pass
an instance of :class:`CustomInstruction` specifying an instruction
name, and this will be evaluated and executed on the robot's side,
if a RAPID procedure with that name exists on the controller.

.. autoclass:: CustomInstruction
   :members:


Utility instructions
====================

.. autoclass:: Noop
   :members:

"""

from __future__ import absolute_import

from .client import *  # noqa: F401, F403
from .common import *  # noqa: F401, F403
from .io import *  # noqa: F401, F403
from .motion import *  # noqa: F401, F403
from .msg import *  # noqa: F401, F403
from .project import *  # noqa: F401, F403
from .utility import *  # noqa: F401, F403
from .watch import *  # noqa: F401, F403

__all__ = [name for name in dir() if not name.startswith('_')]
