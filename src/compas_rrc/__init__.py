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

.. autoclass:: FutureResult
   :members:

Motion instructions
===================

.. autoclass:: MoveAbsJ
   :members:
.. autoclass:: MoveJ
   :members:
.. autoclass:: MoveL
   :members:
.. autoclass:: Zone
   :members:
   :undoc-members:
   :member-order: bysource
.. autoclass:: MotionFeedback
   :members:
   :undoc-members:
   :member-order: bysource

Project-specific instructions
=============================

This library has support for non-standard instructions. Simply pass
an instance of :class:`ProjectInstruction` specifying an instruction
name, and this will be evaluated and executed on the robot's side,
if a RAPID procedure with that name exists on the controller.

.. autoclass:: ProjectInstruction
   :members:
.. autoclass:: ProjectFeedback
   :members:
   :undoc-members:
   :member-order: bysource


"""

from __future__ import absolute_import

from .client import *
from .common import *
from .motion import *
from .project import *
from .new import *

__all__ = [name for name in dir() if not name.startswith('_')]
