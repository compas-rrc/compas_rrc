"""
Request the current frame of the robot.
"""
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc


class CompasRrcGetFrame(component):
    def RunScript(self):
        return rrc.GetFrame()
