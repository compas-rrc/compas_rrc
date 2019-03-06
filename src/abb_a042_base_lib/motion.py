
from compas_fab.backends.ros.messages import ROSmsg


class MoveAbsJ(ROSmsg):
    """Represents a move absolute joint instruction.

    Attributes:
        joints (:obj:`list` of :obj:`float`): Joint positions in degrees.
        ext_axes (:obj:`list` of :obj:`float`): External axes positions, depending
            on the robotic system, it can be millimeters for prismatic external axes, or
            degrees for revolute external axes.
    """

    def __init__(self, joints, ext_axes):
        if len(joints) != 6:
            raise ValueError('Only 6 joints are supported')

        self.joints = joints
        self.ext_axes = ext_axes


if __name__ == '__main__':
    print('Hello world')

    a = MoveAbsJ([90, 45, 34, 1, 10, 20], [10000, -5000, -2000])
    print(a.joints)
