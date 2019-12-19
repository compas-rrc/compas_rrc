import math
import threading

from compas.robots import Joint
from compas_fab.robots import Configuration

__all__ = ['FeedbackLevel',
           'ExecutionLevel',
           'InstructionException',
           'FutureResult',
           'IndustrialConfiguration',
           'ExternalAxes',
           'RobotJoints']


class FeedbackLevel(object):
    """Represents default valid feedback levels."""
    NONE = 0
    DONE = 1


class ExecutionLevel(object):
    """Defines the execution level of an instruction."""
    ROBOT = 0
    RECEIVER = 1
    SENDER = 2
    MASTER = 10


class InstructionException(Exception):
    """Exception caused during/after the execution of an instruction."""

    def __init__(self, message, result):
        super(InstructionException, self).__init__('{}, RRC Reply={}'.format(message, result))
        self.result = result


class FutureResult(object):
    """Represents a future result value.

    Futures are the result of asynchronous operations
    but allow to explicitely control when to block and wait
    for its completion."""

    def __init__(self):
        self.done = False
        self.value = None
        self.event = threading.Event()

    def result(self, timeout=None):
        """Return the feedback value returned by the instruction.

        If the instruction has not yet returned feedback, it will wait
        up to ``timeout`` seconds. If the ``timeout`` expires, the method
        will raise an exception.
        """
        if not self.done:
            if not self.event.wait(timeout):
                raise Exception('Timeout: future result not available')

        if isinstance(self.value, Exception):
            raise self.value

        return self.value

    def _set_result(self, message):
        self.value = message
        self.done = True
        self.event.set()


class IndustrialConfiguration(Configuration):
    """Represents a robot configuration for industrial robots."""

    def __str__(self):
        return '{}, {}'.format(str(self.robot_joints), str(self.external_axes))

    def robot_joints_in_radians(self):
        return self.revolute_values

    def robot_joints_in_degrees(self):
        return [math.degrees(i) for i in self.robot_joints_in_radians()]

    def external_axes_values(self):
        return self.prismatic_values

    @property
    def robot_joints(self):
        return RobotJoints(*self.robot_joints_in_degrees())

    @property
    def external_axes(self):
        return ExternalAxes(*self.external_axes_values())


class ExternalAxes(Configuration):
    """Represents a configuration for external axes"""

    def __init__(self, *positions_in_meters):
        super(ExternalAxes, self).__init__(positions_in_meters, len(positions_in_meters) * [Joint.PRISMATIC])

    def __str__(self):
        return 'External Axes={}'.format([round(i, 2) for i in self.values])

    def __add__(self, other):
        return IndustrialConfiguration(self.values + other.values, self.types + other.types)


class RobotJoints(Configuration):
    """Represents a configuration for robot joints"""

    def __init__(self, *positions_in_degrees):
        super(RobotJoints, self).__init__(list(map(math.radians, positions_in_degrees)), len(positions_in_degrees) * [Joint.REVOLUTE])

    def __str__(self):
        return 'Robot Joints={}'.format([round(math.degrees(i), 2) for i in self.values])

    # TODO: Extend with other operations
    def __add__(self, other):
        return IndustrialConfiguration(self.values + other.values, self.types + other.types)
