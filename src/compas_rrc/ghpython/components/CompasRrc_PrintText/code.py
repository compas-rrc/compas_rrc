"""
Print text on the flex pendant.
"""
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc


class CompasRrcPrintText(component):
    def RunScript(self, text, feedback):
        if not text:
            return (None)

        feedback = feedback or rrc.FeedbackLevel.NONE
        instruction = rrc.PrintText(text, feedback_level=feedback)

        return instruction
