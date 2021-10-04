"""
Wait until the feedback of all instructions has been received.
"""
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc


class CompasRrcWaitForFeedback(component):
    def RunScript(self, results, timeout):
        if not results:
            return (None)

        for future in results:
            if not isinstance(future, rrc.FutureResult):
                raise Exception('Input results must be of type FutureResult. Did you forget to set "Wait for completion" to False in the Execute component?')

        timeout = timeout or 5

        # TODO: This timeout is per future, but the component makes it look like
        # it's a global timeout for all futures together.
        # So this should be fixed and accumulate the total waited time.
        results = [future.result(timeout=timeout) for future in results]

        return results
