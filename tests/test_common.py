import compas_rrc as rrc


def test_robot_joints():
    j = rrc.RobotJoints()
    assert list(j) == []

    j = rrc.RobotJoints(30)
    assert list(j) == [30]

    j = rrc.RobotJoints(30, 10, 0)
    assert list(j) == [30, 10, 0]

    j = rrc.RobotJoints([30, 10, 0])
    assert list(j) == [30, 10, 0]

    j = rrc.RobotJoints(iter([30, 10, 0]))
    assert list(j) == [30, 10, 0]


def test_external_axes():
    ea = rrc.ExternalAxes()
    assert list(ea) == []

    ea = rrc.ExternalAxes(30)
    assert list(ea) == [30]

    ea = rrc.ExternalAxes(30, 10, 0)
    assert list(ea) == [30, 10, 0]

    ea = rrc.ExternalAxes([30, 10, 0])
    assert list(ea) == [30, 10, 0]

    ea = rrc.ExternalAxes(iter([30, 10, 0]))
    assert list(ea) == [30, 10, 0]
