from compas_eve import Message

import compas_rrc as rrc
from compas_rrc.message import Instruction


def test_instruction_is_a_compas_eve_message():
    assert isinstance(rrc.PrintText("hello"), Message)


def test_payload_is_available_as_attributes_and_items():
    inst = rrc.PrintText("hello")

    assert inst.string_values == inst["string_values"] == ["hello"]
    assert inst.msg is inst.data
    assert inst.msg["instruction"] == "r_RRC_PrintText"


def test_missing_attribute_raises_attribute_error():
    # `compas_eve.Message` raises `KeyError` for unknown names, which would make
    # `hasattr()` blow up instead of returning False. The client relies on
    # `hasattr(instruction, "parse_feedback")`.
    inst = rrc.PrintText("hello")

    assert not hasattr(inst, "parse_feedback")
    assert not hasattr(inst, "definitely_not_there")


def test_optional_parse_feedback_is_detected():
    assert hasattr(rrc.ReadWatch(), "parse_feedback")


def test_subclass_without_super_init_still_works():
    # Instructions defined outside this package do not call `super().__init__()`,
    # exactly as they did with the previous `ROSmsg` base class.
    class ThirdPartyInstruction(Instruction):
        def __init__(self):
            self.instruction = "r_RRC_ThirdParty"
            self.float_values = [1.0]

    inst = ThirdPartyInstruction()

    assert inst.msg == {"instruction": "r_RRC_ThirdParty", "float_values": [1.0]}


def test_repr_names_the_class():
    assert repr(rrc.PrintText("hi")).startswith("PrintText(")


def test_debug_exposes_the_wrapped_payload():
    wrapped = rrc.GetJoints()
    debug = rrc.Debug(wrapped)

    # `Debug` delegates through properties; those must win over the payload dict.
    assert debug.msg == wrapped.msg
    assert debug.instruction == wrapped.instruction

    debug.sequence_id = 42
    assert wrapped.sequence_id == 42
    assert debug.msg["sequence_id"] == 42
