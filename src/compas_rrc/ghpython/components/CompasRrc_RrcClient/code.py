"""
Creates an RRC client instance.
"""
from ghpythonlib.component import add_warning
from ghpythonlib.componentbase import executingcomponent as component

import compas_rrc as rrc


class CompasRrcClient(component):
    def RunScript(self, ros_client, namespace):
        if not ros_client:
            add_warning('ros_client is not assigned. The component did not run.')
            self.Message = ''
            return (None)

        kwargs = {}
        if namespace:
            kwargs['namespace'] = namespace

        rrc_client = rrc.AbbClient(ros_client, **kwargs)
        self.Message = 'RRC Client ready'

        return (rrc_client)
