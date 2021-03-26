import itertools
import threading

__all__ = ['CLIENT_PROTOCOL_VERSION',
           'FeedbackLevel',
           'ExecutionLevel',
           'InstructionException',
           'TimeoutException',
           'FutureResult',
           'ExternalAxes',
           'RobotJoints']


CLIENT_PROTOCOL_VERSION = 2


class FeedbackLevel(object):
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


class ExecutionLevel(object):
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

    def __init__(self, message, result):
        super(InstructionException, self).__init__('{}, RRC Reply={}'.format(message, result))
        self.result = result


class TimeoutException(Exception):
    """Timeout exception caused during execution of an instruction."""
    pass


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
                raise TimeoutException('Timeout: future result not available')

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
        return 'ExternalAxes({})'.format([round(i, 2) for i in self.values])

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
        return 'RobotJoints({})'.format([round(i, 2) for i in self.values])

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
