import itertools
import math
import threading

import roslibpy
from compas.robots import Configuration
from compas.robots import Joint
from compas_fab.backends.ros.messages import ROSmsg


__all__ = [
    "CLIENT_PROTOCOL_VERSION",
    "FeedbackLevel",
    "ExecutionLevel",
    "InstructionException",
    "TimeoutException",
    "Interfaces",
    "BaseInstruction",
    "FutureResult",
    "ExternalAxes",
    "RobotJoints",
]

CLIENT_PROTOCOL_VERSION = 2


def _convert_unit_to_meters_radians(value, type_):
    if type_ in {Joint.REVOLUTE, Joint.CONTINUOUS}:
        return math.radians(value)
    return value / 1000.0


def _convert_unit_to_mm_degrees(value, type_):
    if type_ in {Joint.REVOLUTE, Joint.CONTINUOUS}:
        return math.degrees(value)
    return value * 1000.0


class FeedbackLevel(object):
    """Represents default valid feedback levels.

    .. autoattribute:: NONE
    .. autoattribute:: DONE
    .. autoattribute:: DATA
    """

    NONE = 0
    """Indicates no feedback is requested from the robot."""

    DONE = 1
    """Indicates completion feedback is requested from the robot. Completion feedback means
    the robot has executed the procedure. See :meth:`AbbClient.send_and_wait` for more details.
    """

    DATA = -1
    """Indicates all feedback data is requested from the robot."""


class Interfaces(object):
    """Defines the supported interfaces over which instructions can be sent.

    .. autoattribute:: APP
    .. autoattribute:: SYS
    """

    APP = "app"
    """Default interface. Uses the primary TCP/IP communication channels."""

    SYS = "sys"
    """System interafce uses an alternative communication channel. In the case of ABB, web services."""

    SUPPORTED_INTERFACES = (APP, SYS)
    """Tuple of currently-supported interfaces."""


class ExecutionLevel(object):
    """Defines the execution level of an instruction.

    .. autoattribute:: ROBOT
    .. autoattribute:: CONTROLLER
    """

    ROBOT = 0
    """Execute instruction on the robot task."""

    CONTROLLER = 10
    """Execute instruction on the ``controller`` task (only usable with custom instructions)."""

    DRIVER = -1
    """Execute instruction outside of the robot controller, and inside the ROS environment."""


class InstructionException(Exception):
    """Exception caused during/after the execution of an instruction."""

    def __init__(self, message, result):
        super(InstructionException, self).__init__("{}, RRC Reply={}".format(message, result))
        self.result = result


class TimeoutException(Exception):
    """Timeout exception caused during execution of an instruction."""

    pass


class BaseInstruction(ROSmsg):
    """Base class fora all instructions."""

    def __init__(self, instruction_names, default_interface=Interfaces.APP):
        super(BaseInstruction, self).__init__()
        self.meta = dict(instruction_names=instruction_names, interface=default_interface)
        self.feedback_level = FeedbackLevel.NONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def select_interface(self, interface_name):
        """Select the interace over which the instruction will be sent.

        Parameters
        ----------
        interface_name : :obj:`str`
            Name of the interface to select.
        """
        if interface_name not in Interfaces.SUPPORTED_INTERFACES:
            raise ValueError("Interface not supported: {}".format(interface_name))
        self.meta["interface"] = interface_name
        self.instruction = self.meta["instruction_names"].get(interface_name)

        if not self.instruction:
            raise ValueError("Instruction does not support selected interface: '{}'".format(interface_name))

    def supports_interface(self, interface_name):
        """Determines if a specific interface is supported by this instruction.

        Parameters
        ----------
        interface_name : :obj:`str`
            Name of the interface.

        Returns
        -------
        :obj:`bool`
            Indicate whether the interface is supported.
        """
        return interface_name in self.meta["instruction_names"]

    def to_message(self):
        """Convert the instruction to a roslibpy Message instance.

        Returns
        -------
        :class:`roslibpy.Message`
        """
        msg = self.msg
        msg.pop("meta")

        return roslibpy.Message(msg)


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
                raise TimeoutException("Timeout: future result not available")

        if isinstance(self.value, Exception):
            raise self.value

        return self.value

    def _set_result(self, value):
        self.value = value
        self.done = True
        self.event.set()


class ExternalAxes(object):
    """Represents a configuration for external axes."""

    def __init__(self, *values):
        """Initialize a new object with the specified values for external axes.

        Parameters
        ----------
        values : :obj:`list`
            List of floats indicating the external axis positions.
        """
        try:
            self.values = list(itertools.chain.from_iterable(values))
        except TypeError:
            self.values = list(values)

    # Properties
    @property
    def eax_a(self):
        """Value of the first external axis."""
        return self[0]

    @eax_a.setter
    def eax_a(self, value):
        self[0] = value

    @property
    def eax_b(self):
        """Value of the second external axis."""
        return self[1]

    @eax_b.setter
    def eax_b(self, value):
        self[1] = value

    @property
    def eax_c(self):
        """Value of the third external axis."""
        return self[2]

    @eax_c.setter
    def eax_c(self, value):
        self[2] = value

    @property
    def eax_d(self):
        """Value of the fourth external axis."""
        return self[3]

    @eax_d.setter
    def eax_d(self, value):
        self[3] = value

    @property
    def eax_e(self):
        """Value of the fifth external axis."""
        return self[4]

    @eax_e.setter
    def eax_e(self, value):
        self[4] = value

    @property
    def eax_f(self):
        """Value of the sexth external axis."""
        return self[5]

    @eax_f.setter
    def eax_f(self, value):
        self[5] = value

    # List accessors
    def __repr__(self):
        return "ExternalAxes({})".format([round(i, 2) for i in self.values])

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        if item >= len(self.values):
            return None

        return self.values[item]

    def __setitem__(self, item, value):
        self.values[item] = value

    def __iter__(self):
        return iter(self.values)

    # Conversion methods
    def to_configuration_primitive(self, joint_types, joint_names=None):
        """Convert the ExternalAxes to a :class:`compas.robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        joint_types : :obj:`list`
            List of integers representing the joint types of the corresponding external axes values.
        joint_names : :obj:`list`
            List of strings representing the joint names of the corresponding external axes values. Optional.

        Returns
        -------
        :class:`compas.robots.Configuration`
        """
        joint_values = [_convert_unit_to_meters_radians(value, type_) for value, type_ in zip(self.values, joint_types)]
        return Configuration(joint_values, joint_types, joint_names)

    def to_configuration(self, robot, group=None):
        """Convert the ExternalAxes to a :class:`compas.robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        robot : :class:`compas_fab.robots.Robot`
            The robot to be configured.
        group : :obj:`str`
            The name of the group of joints to be included in the ``Configuration``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas.robots.Configuration`
        """
        joint_types = robot.get_configurable_joint_types(group)
        joint_names = robot.get_configurable_joint_names(group)
        return self.to_configuration_primitive(joint_types, joint_names)

    @classmethod
    def from_configuration_primitive(cls, configuration, joint_names=None):
        """Create an instance of ``ExternalAxes`` from a :class:`compas.robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas.robots.Configuration`
            The configuration from which to create the ``ExternalAxes`` instance.
        joint_names : :obj:`list`
            An optional list of joint names from the ``configuration`` whose corresponding
            values will fill the ``ExternalAxes`` values.

        Returns
        -------
        :class:`compas_rrc.ExternalAxes`
        """
        if joint_names:
            joint_values = [
                _convert_unit_to_mm_degrees(configuration[name], configuration.type_dict[name]) for name in joint_names
            ]
        else:
            joint_values = [
                _convert_unit_to_mm_degrees(value, type_)
                for value, type_ in zip(configuration.joint_values, configuration.joint_types)
            ]
        return cls(joint_values)

    @classmethod
    def from_configuration(cls, configuration, robot=None, group=None):
        """Create an instance of ``ExternalAxes`` from a :class:`compas.robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas.robots.Configuration`
            The configuration from which to create the ``ExternalAxes`` instance.
        robot : :class:`compas_fab.robots.Robot`
            The robot to be configured.  Optional.
        group : :obj:`str`
            The name of the group of joints to be included in the ``ExternalAxes``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas_rrc.ExternalAxes`
        """
        joint_names = robot.get_configurable_joint_names(group) if robot else []
        return cls.from_configuration_primitive(configuration, joint_names)


class RobotJoints(object):
    """Represents a configuration for robot joints"""

    def __init__(self, *values):
        try:
            self.values = list(itertools.chain.from_iterable(values))
        except TypeError:
            self.values = list(values)

    # Properties
    @property
    def rax_1(self):
        return self[0]

    @rax_1.setter
    def rax_1(self, value):
        self[0] = value

    @property
    def rax_2(self):
        return self[1]

    @rax_2.setter
    def rax_2(self, value):
        self[1] = value

    @property
    def rax_3(self):
        return self[2]

    @rax_3.setter
    def rax_3(self, value):
        self[2] = value

    @property
    def rax_4(self):
        return self[3]

    @rax_4.setter
    def rax_4(self, value):
        self[3] = value

    @property
    def rax_5(self):
        return self[4]

    @rax_5.setter
    def rax_5(self, value):
        self[4] = value

    @property
    def rax_6(self):
        return self[5]

    @rax_6.setter
    def rax_6(self, value):
        self[5] = value

    # List accessors
    def __repr__(self):
        return "RobotJoints({})".format([round(i, 2) for i in self.values])

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        if item >= len(self.values):
            return None

        return self.values[item]

    def __setitem__(self, item, value):
        self.values[item] = value

    def __iter__(self):
        return iter(self.values)

    # Conversion methods
    def to_configuration_primitive(self, joint_types, joint_names=None):
        """Convert the RobotJoints to a :class:`compas.robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        joint_types : :obj:`list`
            List of integers representing the joint types of the corresponding internal axes values.
        joint_names : :obj:`list`
            List of strings representing the joint names of the corresponding internal axes values. Optional.

        Returns
        -------
        :class:`compas.robots.Configuration`
        """
        joint_values = [_convert_unit_to_meters_radians(value, type_) for value, type_ in zip(self.values, joint_types)]
        return Configuration(joint_values, joint_types, joint_names)

    def to_configuration(self, robot, group=None):
        """Convert the RobotJoints to a :class:`compas.robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        robot : :class:`compas_fab.robots.Robot`
            The robot to be configured.
        group : :obj:`str`
            The name of the group of joints to be included in the ``Configuration``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas.robots.Configuration`
        """
        joint_types = robot.get_configurable_joint_types(group)
        joint_names = robot.get_configurable_joint_names(group)
        return self.to_configuration_primitive(joint_types, joint_names)

    @classmethod
    def from_configuration_primitive(cls, configuration, joint_names=None):
        """Create an instance of ``RobotJoints`` from a :class:`compas.robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas.robots.Configuration`
            The configuration from which to create the ``RobotJoints`` instance.
        joint_names : :obj:`list`
            An optional list of joint names from the ``configuration`` whose corresponding
            values will fill the ``RobotJoints`` values.

        Returns
        -------
        :class:`compas_rrc.RobotJoints`
        """
        if joint_names:
            joint_values = [
                _convert_unit_to_mm_degrees(configuration[name], configuration.type_dict[name]) for name in joint_names
            ]
        else:
            joint_values = [
                _convert_unit_to_mm_degrees(value, type_)
                for value, type_ in zip(configuration.joint_values, configuration.joint_types)
            ]
        return cls(joint_values)

    @classmethod
    def from_configuration(cls, configuration, robot=None, group=None):
        """Create an instance of ``RobotJoints`` from a :class:`compas.robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas.robots.Configuration`
            The configuration from which to create the ``ExternalAxes`` instance.
        robot : :class:`compas_fab.robots.Robot`
            The robot to be configured.  Optional.
        group : :obj:`str`
            The name of the group of joints to be included in the ``ExternalAxes``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas_rrc.RobotJoints`
        """
        joint_names = robot.get_configurable_joint_names(group) if robot else []
        return cls.from_configuration_primitive(configuration, joint_names)
