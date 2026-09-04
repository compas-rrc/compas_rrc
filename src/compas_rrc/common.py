import itertools
import math
import threading
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from compas_robots import Configuration
from compas_robots.model import Joint

__all__ = [
    "CLIENT_PROTOCOL_VERSION",
    "FeedbackLevel",
    "ExecutionLevel",
    "InstructionException",
    "TimeoutException",
    "FutureResult",
    "ExternalAxes",
    "RobotJoints",
]

CLIENT_PROTOCOL_VERSION = 2

Robot = Any
"""Anything exposing ``get_configurable_joint_types`` and ``get_configurable_joint_names``.

This is structural rather than a concrete class, so that a
:class:`compas_fab.robots.RobotCell` works without making ``compas_fab`` a
dependency of this package.
"""


def _convert_unit_to_meters_radians(value: float, type_: int) -> float:
    if type_ in {Joint.REVOLUTE, Joint.CONTINUOUS}:
        return math.radians(value)
    return value / 1000.0


def _convert_unit_to_mm_degrees(value: float, type_: int) -> float:
    if type_ in {Joint.REVOLUTE, Joint.CONTINUOUS}:
        return math.degrees(value)
    return value * 1000.0


class FeedbackLevel:
    """Represents default valid feedback levels.

    .. autoattribute:: NONE
    .. autoattribute:: DONE
    """

    NONE = 0
    """Indicates no feedback is requested from the robot."""

    DONE = 1
    """Indicates completion feedback is requested from the robot. Completion feedback means
    the robot has executed the procedure. See :meth:`AbbClient.send_and_wait` for more details.
    """


class ExecutionLevel:
    """Defines the execution level of an instruction.

    .. autoattribute:: ROBOT
    .. autoattribute:: CONTROLLER
    """

    ROBOT = 0
    """Execute instruction on the robot task."""

    CONTROLLER = 10
    """Execute instruction on the ``controller`` task (only usable with custom instructions)."""


class InstructionException(Exception):
    """Exception caused during/after the execution of an instruction."""

    def __init__(self, message: str, result: Any) -> None:
        super().__init__("{}, RRC Reply={}".format(message, result))
        self.result = result


class TimeoutException(Exception):
    """Timeout exception caused during execution of an instruction."""

    pass


class FutureResult:
    """Represents a future result value.

    Futures are the result of asynchronous operations
    but allow to explicitely control when to block and wait
    for its completion."""

    def __init__(self) -> None:
        self.done = False
        self.value = None
        self.event = threading.Event()

    def result(self, timeout: Optional[float] = None) -> Any:
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

    def _set_result(self, value: Any) -> None:
        self.value = value
        self.done = True
        self.event.set()


class ExternalAxes:
    """Represents a configuration for external axes."""

    def __init__(self, *values: Union[float, List[float]]) -> None:
        """Initialize a new object with the specified values for external axes.

        Parameters
        ----------
        values : :obj:`list`
            List of floats indicating the external axis positions.
        """
        try:
            self.values = list(itertools.chain.from_iterable(values))  # type: ignore[arg-type]
        except TypeError:
            self.values = list(values)  # type: ignore[arg-type]

    # Properties
    @property
    def eax_a(self) -> Optional[float]:
        """Value of the first external axis."""
        return self[0]

    @eax_a.setter
    def eax_a(self, value: float) -> None:
        self[0] = value

    @property
    def eax_b(self) -> Optional[float]:
        """Value of the second external axis."""
        return self[1]

    @eax_b.setter
    def eax_b(self, value: float) -> None:
        self[1] = value

    @property
    def eax_c(self) -> Optional[float]:
        """Value of the third external axis."""
        return self[2]

    @eax_c.setter
    def eax_c(self, value: float) -> None:
        self[2] = value

    @property
    def eax_d(self) -> Optional[float]:
        """Value of the fourth external axis."""
        return self[3]

    @eax_d.setter
    def eax_d(self, value: float) -> None:
        self[3] = value

    @property
    def eax_e(self) -> Optional[float]:
        """Value of the fifth external axis."""
        return self[4]

    @eax_e.setter
    def eax_e(self, value: float) -> None:
        self[4] = value

    @property
    def eax_f(self) -> Optional[float]:
        """Value of the sexth external axis."""
        return self[5]

    @eax_f.setter
    def eax_f(self, value: float) -> None:
        self[5] = value

    # List accessors
    def __repr__(self) -> str:
        return "ExternalAxes({})".format([round(i, 2) for i in self.values])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item: int) -> Optional[float]:
        if item >= len(self.values):
            return None

        return self.values[item]

    def __setitem__(self, item: int, value: float) -> None:
        self.values[item] = value

    def __iter__(self) -> Iterator[float]:
        return iter(self.values)

    # Conversion methods
    def to_configuration_primitive(self, joint_types: List[int], joint_names: Optional[List[str]] = None) -> Configuration:
        """Convert the ExternalAxes to a :class:`compas_robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        joint_types : :obj:`list`
            List of integers representing the joint types of the corresponding external axes values.
        joint_names : :obj:`list`
            List of strings representing the joint names of the corresponding external axes values. Optional.

        Returns
        -------
        :class:`compas_robots.Configuration`
        """
        joint_values = [_convert_unit_to_meters_radians(value, type_) for value, type_ in zip(self.values, joint_types)]
        return Configuration(joint_values, joint_types, joint_names)

    def to_configuration(self, robot: Robot, group: Optional[str] = None) -> Configuration:
        """Convert the ExternalAxes to a :class:`compas_robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        robot : :obj:`object`
            The robot to be configured.
        group : :obj:`str`
            The name of the group of joints to be included in the ``Configuration``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas_robots.Configuration`
        """
        joint_types = robot.get_configurable_joint_types(group)
        joint_names = robot.get_configurable_joint_names(group)
        return self.to_configuration_primitive(joint_types, joint_names)

    @classmethod
    def from_configuration_primitive(cls, configuration: Configuration, joint_names: Optional[List[str]] = None) -> "ExternalAxes":
        """Create an instance of ``ExternalAxes`` from a :class:`compas_robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas_robots.Configuration`
            The configuration from which to create the ``ExternalAxes`` instance.
        joint_names : :obj:`list`
            An optional list of joint names from the ``configuration`` whose corresponding
            values will fill the ``ExternalAxes`` values.

        Returns
        -------
        :class:`compas_rrc.ExternalAxes`
        """
        if joint_names:
            joint_values = [_convert_unit_to_mm_degrees(configuration[name], configuration.type_dict[name]) for name in joint_names]
        else:
            joint_values = [_convert_unit_to_mm_degrees(value, type_) for value, type_ in zip(configuration.joint_values, configuration.joint_types)]
        return cls(joint_values)

    @classmethod
    def from_configuration(cls, configuration: Configuration, robot: Optional[Robot] = None, group: Optional[str] = None) -> "ExternalAxes":
        """Create an instance of ``ExternalAxes`` from a :class:`compas_robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas_robots.Configuration`
            The configuration from which to create the ``ExternalAxes`` instance.
        robot : :obj:`object`
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


class RobotJoints:
    """Represents a configuration for robot joints"""

    def __init__(self, *values: Union[float, List[float]]) -> None:
        try:
            self.values = list(itertools.chain.from_iterable(values))  # type: ignore[arg-type]
        except TypeError:
            self.values = list(values)  # type: ignore[arg-type]

    # Properties
    @property
    def rax_1(self) -> Optional[float]:
        return self[0]

    @rax_1.setter
    def rax_1(self, value: float) -> None:
        self[0] = value

    @property
    def rax_2(self) -> Optional[float]:
        return self[1]

    @rax_2.setter
    def rax_2(self, value: float) -> None:
        self[1] = value

    @property
    def rax_3(self) -> Optional[float]:
        return self[2]

    @rax_3.setter
    def rax_3(self, value: float) -> None:
        self[2] = value

    @property
    def rax_4(self) -> Optional[float]:
        return self[3]

    @rax_4.setter
    def rax_4(self, value: float) -> None:
        self[3] = value

    @property
    def rax_5(self) -> Optional[float]:
        return self[4]

    @rax_5.setter
    def rax_5(self, value: float) -> None:
        self[4] = value

    @property
    def rax_6(self) -> Optional[float]:
        return self[5]

    @rax_6.setter
    def rax_6(self, value: float) -> None:
        self[5] = value

    # List accessors
    def __repr__(self) -> str:
        return "RobotJoints({})".format([round(i, 2) for i in self.values])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item: int) -> Optional[float]:
        if item >= len(self.values):
            return None

        return self.values[item]

    def __setitem__(self, item: int, value: float) -> None:
        self.values[item] = value

    def __iter__(self) -> Iterator[float]:
        return iter(self.values)

    # Conversion methods
    def to_configuration_primitive(self, joint_types: List[int], joint_names: Optional[List[str]] = None) -> Configuration:
        """Convert the RobotJoints to a :class:`compas_robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        joint_types : :obj:`list`
            List of integers representing the joint types of the corresponding internal axes values.
        joint_names : :obj:`list`
            List of strings representing the joint names of the corresponding internal axes values. Optional.

        Returns
        -------
        :class:`compas_robots.Configuration`
        """
        joint_values = [_convert_unit_to_meters_radians(value, type_) for value, type_ in zip(self.values, joint_types)]
        return Configuration(joint_values, joint_types, joint_names)

    def to_configuration(self, robot: Robot, group: Optional[str] = None) -> Configuration:
        """Convert the RobotJoints to a :class:`compas_robots.Configuration`, including the unit conversion
        from mm and degrees to meters and radians.

        Parameters
        ----------
        robot : :obj:`object`
            The robot to be configured.
        group : :obj:`str`
            The name of the group of joints to be included in the ``Configuration``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas_robots.Configuration`
        """
        joint_types = robot.get_configurable_joint_types(group)
        joint_names = robot.get_configurable_joint_names(group)
        return self.to_configuration_primitive(joint_types, joint_names)

    @classmethod
    def from_configuration_primitive(cls, configuration: Configuration, joint_names: Optional[List[str]] = None) -> "RobotJoints":
        """Create an instance of ``RobotJoints`` from a :class:`compas_robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas_robots.Configuration`
            The configuration from which to create the ``RobotJoints`` instance.
        joint_names : :obj:`list`
            An optional list of joint names from the ``configuration`` whose corresponding
            values will fill the ``RobotJoints`` values.

        Returns
        -------
        :class:`compas_rrc.RobotJoints`
        """
        if joint_names:
            joint_values = [_convert_unit_to_mm_degrees(configuration[name], configuration.type_dict[name]) for name in joint_names]
        else:
            joint_values = [_convert_unit_to_mm_degrees(value, type_) for value, type_ in zip(configuration.joint_values, configuration.joint_types)]
        return cls(joint_values)

    @classmethod
    def from_configuration(cls, configuration: Configuration, robot: Optional[Robot] = None, group: Optional[str] = None) -> "RobotJoints":
        """Create an instance of ``RobotJoints`` from a :class:`compas_robots.Configuration`, including the unit
        conversion from meters and radians to mm and degrees.

        Parameters
        ----------
        configuration : :class:`compas_robots.Configuration`
            The configuration from which to create the ``RobotJoints`` instance.
        robot : :obj:`object`
            The robot to be configured.  Optional.
        group : :obj:`str`
            The name of the group of joints to be included in the ``RobotJoints``. Optional.
            Defaults to the ``robot``'s main group name.

        Returns
        -------
        :class:`compas_rrc.RobotJoints`
        """
        joint_names = robot.get_configurable_joint_names(group) if robot else []
        return cls.from_configuration_primitive(configuration, joint_names)
