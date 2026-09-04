"""Transport-agnostic message types for COMPAS RRC.

The RRC wire protocol is deliberately flat: a message carries an instruction
name, an execution level, a feedback level, a sequence id, and two lists of
values, one of strings and one of floats. That is barely more than a
dictionary, which is exactly what :class:`compas_eve.Message` models.

Building the instructions on top of ``compas_eve`` means they are not tied to
ROS: the same instruction object can be published over any ``compas_eve``
transport. ROS carries it in the driver's native ``RobotMessage`` type; other
transports carry the payload themselves and encode it with a codec.
"""

from compas_eve import Message

__all__ = ["RobotMessage", "Instruction"]


class RobotMessage(Message):
    """A message exchanged with an RRC driver.

    The payload lives in :attr:`data` and is reachable both as attributes and
    as items, so ``message.float_values`` and ``message["float_values"]`` are
    the same thing.

    Notes
    -----
    Subclasses are not required to call ``super().__init__()`` before assigning
    attributes. This mirrors how the previous ``ROSmsg`` base class behaved and
    keeps instructions defined outside this package working.
    """

    ROS_MSG_TYPE = "compas_rrc_driver/RobotMessage"
    """:obj:`str`: Name of the ROS message type used to carry these messages."""

    def __getattr__(self, name):
        # `Message` keeps every value in `data` and raises `KeyError` for names
        # it does not hold. Attribute lookup has to raise `AttributeError`
        # instead, otherwise `hasattr()` propagates the `KeyError` -- which is
        # how the client tests for an optional `parse_feedback` on
        # an instruction.
        if name == "data" or name.startswith("__"):
            raise AttributeError(name)

        try:
            return self.data[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, key, value):
        # `hasattr(type(self), key)` keeps properties working: `Debug` exposes the
        # wrapped instruction through them, and those must not be shadowed by a
        # plain entry in `data`.
        if key == "data" or key in self.__dict__ or hasattr(type(self), key):
            object.__setattr__(self, key, value)
            return

        # Create the payload lazily so that a subclass can assign attributes in
        # its `__init__` without calling `super().__init__()` first.
        if "data" not in self.__dict__:
            object.__setattr__(self, "data", {})

        self.data[key] = value

    @property
    def msg(self):
        """:obj:`dict`: The message payload as a plain dictionary."""
        return self.data

    def __repr__(self):
        args = ", ".join("{}={!r}".format(key, value) for key, value in self.data.items())
        return "{}({})".format(type(self).__name__, args)


class Instruction(RobotMessage):
    """Base class for all COMPAS RRC instructions.

    An instruction is a message sent *to* the robot. Concrete instructions set
    ``instruction``, ``exec_level``, ``feedback_level``, ``string_values`` and
    ``float_values`` in their constructor, and may define a ``parse_feedback``
    method to turn the robot's response into a useful Python value.
    """
