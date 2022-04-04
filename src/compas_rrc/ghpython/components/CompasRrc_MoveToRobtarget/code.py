"""
Move robot to the specified robtarget in cartesian space.
"""
from ghpythonlib.component import add_error
from ghpythonlib.component import add_warning
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc
from compas_rrc.ghpython import coerce_frame


class CompasRrcMoveToRobtarget(component):
    def __init__(self):
        super(CompasRrcMoveToRobtarget, self).__init__()
        self.motion_type = rrc.Motion.JOINT

    def RunScript(self, frame, external_axes, speed, zone, feedback):
        if not frame:
            add_warning('Frame is not defined. The component did not run.')
            return None

        if not external_axes:
            add_warning('External axes is not defined. The component did not run.')
            return None

        if not speed or speed < 0.01:
            add_warning('Speed must be greater or equal to 0.01 mm/s.')
            return None

        if not zone:
            zone = rrc.Zone.FINE

        frame = coerce_frame(frame)
        feedback = feedback or rrc.FeedbackLevel.NONE
        instruction = rrc.MoveToRobtarget(frame, external_axes, speed, zone, motion_type=self.motion_type, feedback_level=feedback)
        self.Message = '{} Motion'.format('Joint' if self.motion_type == rrc.Motion.JOINT else 'Linear')

        return instruction

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
