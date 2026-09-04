# isort: skip_file
"""Library of instructions for ABB robots using the COMPAS RRC driver.

Everything is re-exported from this top-level package, so ``import compas_rrc as rrc``
is normally all that is needed. See the documentation for the main concepts and the
full instruction reference: https://compas-rrc.github.io/compas_rrc
"""

from compas_rrc.__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __license__,
    __url__,
    __version__,
)
from compas_rrc.client import AbbClient, RosClient
from compas_rrc.common import (
    CLIENT_PROTOCOL_VERSION,
    ExecutionLevel,
    ExternalAxes,
    FeedbackLevel,
    FutureResult,
    InstructionException,
    RobotJoints,
    TimeoutException,
)
from compas_rrc.custom import CustomInstruction
from compas_rrc.io import (
    PulseDigital,
    ReadAnalog,
    ReadDigital,
    ReadGroup,
    SetAnalog,
    SetDigital,
    SetGroup,
)
from compas_rrc.motion import Motion, MoveToFrame, MoveToJoints, MoveToRobtarget, Zone
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
    WaitTime,
)
from compas_rrc.watch import ReadWatch, StartWatch, StopWatch

__all__ = [
    "__url__",
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "CLIENT_PROTOCOL_VERSION",
    "FeedbackLevel",
    "ExecutionLevel",
    "InstructionException",
    "TimeoutException",
    "FutureResult",
    "ExternalAxes",
    "RobotJoints",
    "RosClient",
    "AbbClient",
    "SetDigital",
    "SetAnalog",
    "SetGroup",
    "PulseDigital",
    "ReadAnalog",
    "ReadDigital",
    "ReadGroup",
    "Zone",
    "Motion",
    "MoveToJoints",
    "MoveToFrame",
    "MoveToRobtarget",
    "PrintText",
    "CustomInstruction",
    "Noop",
    "GetFrame",
    "GetJoints",
    "GetRobtarget",
    "SetAcceleration",
    "SetTool",
    "SetMaxSpeed",
    "Stop",
    "WaitTime",
    "SetWorkObject",
    "Debug",
    "ReadWatch",
    "StartWatch",
    "StopWatch",
]
