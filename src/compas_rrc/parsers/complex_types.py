"""
The following classes are not currently stable, so they are not added to the public API.

This will probably change in the near future.
"""
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Quaternion


def parse_complex_type(value, type_name, type_namespace):
    ns = SUPPORTED_COMPLEX_TYPES.get(type_namespace)
    cls = ns.get(type_name) if ns else None

    # No supported complex type, return what we have
    if not cls:
        return value

    return cls.from_list(value)


class LoadData(object):
    def __init__(self, mass, center_of_gravity, axes_of_moment, ix, iy, iz):
        self.mass = mass
        self.center_of_gravity = (
            center_of_gravity if isinstance(center_of_gravity, Point) else Point(*center_of_gravity)
        )

        if isinstance(axes_of_moment, Quaternion):
            self.axes_of_moment = axes_of_moment
        else:
            # TODO: verify if the ABB quaternion is really xyzw
            q = axes_of_moment
            w, x, y, z = q[3], q[0], q[1], q[2]
            self.axes_of_moment = Quaternion(w, x, y, z)
        self.ix = ix
        self.iy = iy
        self.iz = iz

    @classmethod
    def from_list(cls, value):
        return cls(*value)


class ToolData(object):
    def __init__(self, robot_hold, frame, load_data):
        self.robot_hold = robot_hold
        self.frame = frame
        self.load_data = load_data

    @classmethod
    def from_list(cls, value):
        robot_hold = value[0]
        frame_point, q = value[1]
        load_data = value[2]

        # TODO: verify if the ABB quaternion is really xyzw
        w, x, y, z = q[3], q[0], q[1], q[2]
        frame = Frame.from_quaternion([w, x, y, z], point=frame_point)

        return cls(robot_hold, frame, LoadData.from_list(load_data))


SUPPORTED_COMPLEX_TYPES = {}
SUPPORTED_COMPLEX_TYPES["abb"] = {
    "tooldata": ToolData,
    "loaddata": LoadData,
}
