"""
The following classes are not currently stable, so they are not added to the public API.

This will probably change in the near future.
"""
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Quaternion


# decode
def decode(value, type_name, type_namespace):
    ns = DECODERS.get(type_namespace)
    decoder = ns.get(type_name) if ns else None

    # No supported complex type, return what we have
    if not decoder:
        return value

    return decoder().decode(value)


# encode
def encode(value, type_namespace):
    ns = ENCODERS.get(type_namespace)
    encoder = ns.get(type(value)) if ns else None

    # No supported complex type, return what we have
    if not encoder:
        return value

    return encoder().encode(value)


class TypeEncoder(object):
    def encode(self, value):
        pass


class TypeDecoder(object):
    def decode(self, value):
        pass


class LoadData(object):
    def __init__(self, mass, center_of_gravity, axes_of_moment, ix, iy, iz):
        self.mass = mass
        self.center_of_gravity = (
            center_of_gravity if isinstance(center_of_gravity, Point) else Point(*center_of_gravity)
        )

        if isinstance(axes_of_moment, Quaternion):
            self.axes_of_moment = axes_of_moment
        else:
            q = axes_of_moment
            w, x, y, z = q[3], q[0], q[1], q[2]
            self.axes_of_moment = Quaternion(w, x, y, z)
        self.ix = ix
        self.iy = iy
        self.iz = iz

    def __repr__(self):
        return "LoadData({}, {}, {}, {}, {}, {})".format(
            self.mass, repr(self.center_of_gravity), repr(self.axes_of_moment), self.ix, self.iy, self.iz
        )


class LoadDataDecoder(TypeDecoder):
    def decode(self, value):
        return LoadData(*value)


class LoadDataEncoder(TypeEncoder):
    def encode(self, value):
        return [
            value.mass,
            [value.center_of_gravity.x, value.center_of_gravity.y, value.center_of_gravity.z],
            value.axes_of_moment.xyzw,
            value.ix,
            value.iy,
            value.iz,
        ]


class ToolData(object):
    def __init__(self, robot_hold, frame, load_data):
        self.robot_hold = robot_hold
        self.frame = frame
        self.load_data = load_data


class ToolDataDecoder(TypeDecoder):
    def decode(self, value):
        robot_hold = value[0]
        frame_point, q = value[1]
        load_data = value[2]

        w, x, y, z = q[3], q[0], q[1], q[2]
        frame = Frame.from_quaternion([w, x, y, z], point=frame_point)

        # TODO: consider replacing decode(load_data, 'loaddata', 'abb') with LoadDataDecoder().decode()
        return ToolData(robot_hold, frame, decode(load_data, "loaddata", "abb"))


class ToolDataEncoder(TypeEncoder):
    def encode(self, value):
        type_namespace = "abb"
        return [value.robot_hold, encode(value.frame, type_namespace), encode(value.load_data, type_namespace)]


class FrameEncoder(TypeEncoder):
    def encode(self, value):
        return [[value.point.x, value.point.y, value.point.z], value.quaternion.xyzw]


DECODERS = {}
ENCODERS = {}
DECODERS["abb"] = {
    "tooldata": ToolDataDecoder,
    "loaddata": LoadDataDecoder,
}
ENCODERS["abb"] = {
    ToolData: ToolDataEncoder,
    LoadData: LoadDataEncoder,
    Frame: FrameEncoder,
}
