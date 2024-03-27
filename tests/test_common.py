import math

from compas.geometry import allclose
from compas_robots import Configuration
import compas_rrc as rrc


def test__convert_units():
    v = rrc.common._convert_unit_to_meters_radians(180, 0)
    assert v == math.pi

    v = rrc.common._convert_unit_to_meters_radians(-180, 1)
    assert v == -math.pi

    v = rrc.common._convert_unit_to_meters_radians(2545, 2)
    assert v == 2.545

    v = rrc.common._convert_unit_to_mm_degrees(math.pi, 0)
    assert v == 180

    v = rrc.common._convert_unit_to_mm_degrees(-math.pi, 1)
    assert v == -180

    v = rrc.common._convert_unit_to_mm_degrees(2.545, 2)
    assert v == 2545


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
    c = j.to_configuration_primitive([0, 1, 2], ["j1", "j2", "j3"])
    assert c.joint_values == [math.pi / 6, math.pi / 4, 0.0]
    assert c.joint_names == ["j1", "j2", "j3"]

    j = rrc.RobotJoints(30, -45, 100)
    c = j.to_configuration_primitive([0, 1, 2])
    assert c.joint_values == [math.pi / 6, -math.pi / 4, 0.1]
    assert len(c.joint_names) == 0

    config = Configuration(
        [2 * math.pi, math.pi, math.pi / 2, math.pi / 3, math.pi / 4, math.pi / 6],
        [0, 0, 0, 0, 0, 0],
    )
    rj = rrc.RobotJoints.from_configuration_primitive(config)
    assert allclose(rj.values, [360, 180, 90, 60, 45, 30])

    config = Configuration(
        [0, 2 * math.pi, math.pi, math.pi / 2, math.pi / 3, math.pi / 4, math.pi / 6],
        [0, 0, 0, 0, 0, 0, 0],
        ["a", "b", "c", "d", "e", "f", "g"],
    )
    rj = rrc.RobotJoints.from_configuration_primitive(
        config, ["b", "c", "d", "e", "f", "g"]
    )
    assert allclose(rj.values, [360, 180, 90, 60, 45, 30])

    j = rrc.RobotJoints(30, 10, 0)
    config = j.to_configuration_primitive([0, 0, 0])
    new_j = rrc.RobotJoints.from_configuration_primitive(config)
    assert allclose(j.values, new_j.values)


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
    c = j.to_configuration_primitive([0, 1, 2], ["j1", "j2", "j3"])
    assert c.joint_values == [math.pi / 6, math.pi / 4, 0.0]
    assert c.joint_names == ["j1", "j2", "j3"]

    j = rrc.ExternalAxes(30, -45, 100)
    c = j.to_configuration_primitive([0, 1, 2])
    assert c.joint_values == [math.pi / 6, -math.pi / 4, 0.1]
    assert len(c.joint_names) == 0

    config = Configuration(
        [2 * math.pi, math.pi, math.pi / 2, math.pi / 3, math.pi / 4, math.pi / 6],
        [0, 0, 0, 0, 0, 0],
    )
    rj = rrc.ExternalAxes.from_configuration_primitive(config)
    assert allclose(rj.values, [360, 180, 90, 60, 45, 30])

    config = Configuration(
        [0, 2 * math.pi, math.pi, math.pi / 2, math.pi / 3, math.pi / 4, math.pi / 6],
        [0, 0, 0, 0, 0, 0, 0],
        ["a", "b", "c", "d", "e", "f", "g"],
    )
    rj = rrc.ExternalAxes.from_configuration_primitive(
        config, ["b", "c", "d", "e", "f", "g"]
    )
    assert allclose(rj.values, [360, 180, 90, 60, 45, 30])

    j = rrc.RobotJoints(30, 10, 0)
    config = j.to_configuration_primitive([0, 0, 0])
    new_j = rrc.ExternalAxes.from_configuration_primitive(config)
    assert allclose(j.values, new_j.values)
