"""End-to-end tests over an in-memory transport.

These exercise the full client path -- protocol version handshake, publishing
an instruction, receiving feedback and resolving the future -- without ROS,
which is the point of building on `compas_eve`.
"""

from compas_eve import Message
from compas_eve import Publisher
from compas_eve import Subscriber
from compas_eve import Topic
from compas_eve.memory import InMemoryTransport

import compas_rrc as rrc
from compas_rrc.message import RobotMessage


class FakeDriver:
    """Minimal stand-in for the RRC driver, speaking the protocol over any transport."""

    def __init__(self, transport, namespace="/rob1/", protocol_version=rrc.CLIENT_PROTOCOL_VERSION):
        self.transport = transport
        self.received = []

        Publisher(Topic(namespace + "protocol_version", Message), transport=transport).publish(
            {"data": str(protocol_version)},
            retain=True,
        )

        self._responses = Publisher(Topic(namespace + "robot_response", RobotMessage), transport=transport)
        self._commands = Subscriber(
            Topic(namespace + "robot_command", RobotMessage),
            callback=self._on_command,
            transport=transport,
        )
        self._commands.subscribe()

    def _on_command(self, message):
        self.received.append(message)

        if message["feedback_level"] > 0:
            self._responses.publish(
                {
                    "feedback_id": message["sequence_id"],
                    "feedback": "Done",
                    "float_values": [42.0],
                    "string_values": [],
                }
            )


def test_send_without_feedback():
    transport = InMemoryTransport()
    driver = FakeDriver(transport)
    abb = rrc.AbbClient(transport, "/rob1")

    assert abb.send(rrc.PrintText("hello")) is None
    assert len(driver.received) == 1
    assert driver.received[0]["instruction"] == "r_RRC_PrintText"
    assert driver.received[0]["string_values"] == ["hello"]


def test_send_and_wait_resolves_the_future():
    transport = InMemoryTransport()
    FakeDriver(transport)
    abb = rrc.AbbClient(transport, "/rob1")

    assert abb.send_and_wait(rrc.PrintText("hello"), timeout=5) == "Done"


def test_send_and_wait_runs_the_instruction_parser():
    transport = InMemoryTransport()
    FakeDriver(transport)
    abb = rrc.AbbClient(transport, "/rob1")

    # ReadWatch parses the first float value and rounds it.
    assert abb.send_and_wait(rrc.ReadWatch(), timeout=5) == 42.0


def test_sequence_ids_increment_across_instructions():
    transport = InMemoryTransport()
    driver = FakeDriver(transport)
    abb = rrc.AbbClient(transport, "/rob1")

    abb.send(rrc.PrintText("one"))
    abb.send(rrc.PrintText("two"))

    assert [message["sequence_id"] for message in driver.received] == [1, 2]


def test_protocol_version_mismatch_is_reported():
    transport = InMemoryTransport()
    FakeDriver(transport, protocol_version=rrc.CLIENT_PROTOCOL_VERSION + 1)
    abb = rrc.AbbClient(transport, "/rob1")

    try:
        abb.send(rrc.PrintText("hello"))
    except Exception as exception:
        assert "Protocol version mismatch" in str(exception)
    else:
        raise AssertionError("Expected a protocol version mismatch")


def test_ros_topics_use_the_native_message_type():
    import roslibpy

    from compas_rrc.client import _as_transport
    from compas_rrc.client import _protocol_version_topic
    from compas_rrc.client import _robot_message_topic

    # Constructing a roslibpy client does not connect; `run()` would.
    transport = _as_transport(roslibpy.Ros(host="localhost", port=9090))

    command = _robot_message_topic(transport, "/rob1/robot_command", queue_size=None)
    assert command.message_type == "compas_rrc_driver/RobotMessage"
    assert command.options == {"queue_size": None}

    version = _protocol_version_topic(transport, "/rob1/protocol_version")
    assert version.message_type == "std_msgs/String"


def test_other_transports_carry_the_payload_themselves():
    from compas_rrc.client import _protocol_version_topic
    from compas_rrc.client import _robot_message_topic

    transport = InMemoryTransport()

    assert _robot_message_topic(transport, "/rob1/robot_command", queue_size=None).message_type is RobotMessage
    assert _protocol_version_topic(transport, "/rob1/protocol_version").message_type is Message


def test_unsupported_connection_object_is_rejected():
    from compas_rrc.client import _as_transport

    try:
        _as_transport("localhost")
    except TypeError as exception:
        assert "compas_eve transport" in str(exception)
    else:
        raise AssertionError("Expected a TypeError")
