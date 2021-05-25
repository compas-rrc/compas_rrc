import math

from compas.robots import Configuration
import compas_rrc as rrc


def test__convert_units():
    v = rrc.common._convert_unit(180, 0)
    assert v == math.pi

    v = rrc.common._convert_unit(-180, 1)
    assert v == -math.pi

    v = rrc.common._convert_unit(2545, 2)
    assert v == 2.545


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

    j = rrc.RobotJoints(30, 45, 0)
    c = j.to_configuration_primitive([0, 1, 2], ['j1', 'j2', 'j3'])
    assert c.joint_values == [math.pi/6, math.pi/4, 0.0]
    assert c.joint_names == ['j1', 'j2', 'j3']

    j = rrc.RobotJoints(30, -45, 100)
    c = j.to_configuration_primitive([0, 1, 2])
    assert c.joint_values == [math.pi/6, -math.pi/4, 0.1]
    assert len(c.joint_names) == 0

    config = Configuration([0, 1, 2, 3, 4, 5], [0, 0, 0, 0, 0, 0])
    rj = rrc.RobotJoints.from_configuration_primitive(config)
    assert rj.rax_1 == 0
    assert rj.rax_6 == 5

    config = Configuration([0, 1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0, 0], ['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    rj = rrc.RobotJoints.from_configuration_primitive(config, ['b', 'c', 'd', 'e', 'f', 'g'])
    assert rj.rax_1 == 1
    assert rj.rax_6 == 6


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

    j = rrc.ExternalAxes(30, 45, 0)
    c = j.to_configuration_primitive([0, 1, 2], ['j1', 'j2', 'j3'])
    assert c.joint_values == [math.pi/6, math.pi/4, 0.0]
    assert c.joint_names == ['j1', 'j2', 'j3']

    j = rrc.ExternalAxes(30, -45, 100)
    c = j.to_configuration_primitive([0, 1, 2])
    assert c.joint_values == [math.pi/6, -math.pi/4, 0.1]
    assert len(c.joint_names) == 0

    config = Configuration([0, 1, 2, 3, 4, 5], [0, 0, 0, 0, 0, 0])
    rj = rrc.ExternalAxes.from_configuration_primitive(config)
    assert rj.eax_a == 0
    assert rj.eax_f == 5

    config = Configuration([0, 1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0, 0], ['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    rj = rrc.ExternalAxes.from_configuration_primitive(config, ['b', 'c', 'd', 'e', 'f', 'g'])
    assert rj.eax_a == 1
    assert rj.eax_f == 6
