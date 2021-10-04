"""
Move robot to the specified frame in cartesian space.
"""
from ghpythonlib.component import add_error
from ghpythonlib.component import add_warning
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc
from compas_rrc.ghpython import coerce_frame


class CompasRrcMoveToFrame(component):
    def __init__(self):
        super(CompasRrcMoveToFrame, self).__init__()
        self.motion_type = rrc.Motion.JOINT

    def RunScript(self, frame, speed, zone, feedback):
        if not frame:
            add_warning('Frame is not defined. The component did not run.')
            return (None)

        if not speed or speed < 0.01:
            add_warning('Speed must be greater or equal to 0.01 mm/s.')
            return (None)

        if not zone:
            zone = rrc.Zone.FINE

        frame = coerce_frame(frame)
        feedback = feedback or rrc.FeedbackLevel.NONE
        ins = rrc.MoveToFrame(frame, speed, zone, motion_type=self.motion_type, feedback_level=feedback)

        return (ins)

    def OnTextMenuClick(self, _sender, _args):
        try:
            self.motion_type = rrc.Motion.JOINT if self.motion_type == rrc.Motion.LINEAR else rrc.Motion.LINEAR
            self.ExpireSolution(True)
        except Exception as ex:
            add_error(str(ex))

    def AppendAdditionalMenuItems(self, items):
        component.AppendAdditionalMenuItems(self, items)

        try:
            image = None
            item = items.Items.Add('Move in joint space', image, self.OnTextMenuClick)
            item.Checked = self.motion_type == rrc.Motion.JOINT
        except Exception as ex:
            add_error(str(ex))
