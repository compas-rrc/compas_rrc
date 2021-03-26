import pytest
from compas.geometry import Frame

import compas_rrc as rrc


def test_move_to_joints():
    joints = [30, 90, 0, 0, 0]
    extaxe = [0, 0, 100]
    inst = rrc.MoveToJoints(joints, extaxe, 100, rrc.Zone.FINE)

    assert inst.float_values == [30, 90, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, -1]
    assert not inst.string_values
    assert inst.exec_level == rrc.ExecutionLevel.ROBOT
    assert inst.feedback_level == rrc.FeedbackLevel.NONE

    joints = rrc.RobotJoints(30, 90, 0, 0, 0)
    extaxe = rrc.ExternalAxes(0, 0, 100)
    inst = rrc.MoveToJoints(joints, extaxe, 100, rrc.Zone.FINE)

    assert inst.float_values == [30, 90, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 100, -1]


def test_move_to_joints_validation():
    # Only up to 6 joints are supported
    with pytest.raises(ValueError):
        rrc.MoveToJoints([30, 90, 0, 0, 0, 0, 0, 0], [0, 0, 100], 100, rrc.Zone.FINE)

    # Only up to 6 external axes are supported
    with pytest.raises(ValueError):
        rrc.MoveToJoints([30, 90], [0, 0, 100, 0, 0, 0, 0], 100, rrc.Zone.FINE)


def test_move_to_frame():
    inst = rrc.MoveToFrame(Frame.worldXY(), 100, rrc.Zone.FINE, rrc.Motion.JOINT)

    assert inst.float_values == [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 100, -1]
    assert inst.string_values == ['FrameJ']

    inst = rrc.MoveToFrame(Frame.worldXY(), 100, rrc.Zone.FINE, rrc.Motion.LINEAR)
    assert inst.string_values == ['FrameL']


def test_move_to_robtarget():
    inst = rrc.MoveToRobtarget(Frame.worldXY(), [50, 20], 100, rrc.Zone.FINE, rrc.Motion.JOINT)

    assert inst.float_values == [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 50, 20, 0, 0, 0, 0, 100, -1]
    assert inst.string_values == ['J']


def test_move_to_robtarget_validation():
    # Only up to 6 external axes are supported
    with pytest.raises(ValueError):
        rrc.MoveToRobtarget(Frame.worldXY(), [50, 20, 0, 0, 0, 0, 0, 0], 100, rrc.Zone.FINE, rrc.Motion.JOINT)
