"""

.. currentmodule:: compas_rrc

The API of ``COMPAS RRC`` is minimal and very easy to understand.

Communication methods
=====================

The primary way to interact with robots is using the client classes. They allow four
methods of communication:

 * ``send`` : Sends a command without waiting for feedback.
 * ``send`` in the future : Sends a command without waiting for feedback.
 * ``send_and_wait`` : Sends a command and waits for the robot
   to respond before continuing to the next line of code.
 * ``send_and_subscribe`` : XXXXX

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AbbClient
    ExecutionLevel

Handling feedback
-----------------

For cases in which you wish to send a command and wait for feedback, the
easiest option is to use ``send_and_wait``, but for fine-grained control of
when to wait for feedback, the ``send`` methods returns an object of type
:class:`FutureResult`. The call is non-blocking, so it returns immediatelly
but when the ``result()`` method of the future result is invoked, it will block
until the result is eventually available.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    FutureResult
    FeedbackLevel

Robot joints and External axes
==============================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotJoints
    ExternalAxes

Custom instructions
===================

This library has support for non-standard instructions. Simply pass
an instance of :class:`CustomInstruction` specifying an instruction
name, and this will be evaluated and executed on the robot's side,
if a RAPID procedure with that name exists on the controller.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CustomInstruction

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
