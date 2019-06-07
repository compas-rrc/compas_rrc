import threading


class ExecutionLevel(object):
    ROBOT = 0
    RECEIVER = 1
    SENDER = 2
    MASTER = 10

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

        return self.value

    def _set_result(self, message):
        self.value = message
        self.done = True
        self.event.set()
