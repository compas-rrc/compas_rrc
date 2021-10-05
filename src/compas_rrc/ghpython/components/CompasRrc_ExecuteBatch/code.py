"""
Execute a batch of instructions.
"""
from ghpythonlib.component import add_error
from ghpythonlib.component import add_warning
from ghpythonlib.componentbase import executingcomponent as component
from scriptcontext import sticky as st

import compas_rrc as rrc
from compas_rrc.ghpython import create_id


class CompasRrcExecuteBatch(component):
    TIMEOUT = 60

    def __init__(self):
        super(CompasRrcExecuteBatch, self).__init__()
        self.wait_for_completion = True

    def RunScript(self, rrc_client, instructions, run):
        if not rrc_client:
            add_warning('rrc_client is not assigned. The component did not run.')
            self.Message = ''
            return False, None

        if len(instructions) == 0:
            self.Message = 'No instructions'
            return False, None

        run_key = create_id(self, 'run_status')
        res_key = create_id(self, 'results')

        # TODO: Add checks for rrc_client.ros.is_connected before attempting to execute
        if run:
            futures = []
            for instruction in instructions[:-1]:
                future = rrc_client.send(instruction)
                if instruction.feedback_level > rrc.FeedbackLevel.NONE:
                    futures.append(future)

            last_instruction = instructions[-1]

            if not self.wait_for_completion:
                future = rrc_client.send(last_instruction)
                if last_instruction.feedback_level > rrc.FeedbackLevel.NONE:
                    futures.append(future)

                # In the non-wait mode, the results are futures
                results = futures
            else:
                feedback = rrc_client.send_and_wait(last_instruction, timeout=self.TIMEOUT)

                # Since we wait for the last instruction, all previous ones
                # must have completed as well, so we can collect their futures
                results = [future.result(timeout=self.TIMEOUT) for future in futures]
                results.append(feedback)

            self.Message = 'Executed {} actions'.format(len(instructions))
            st[run_key] = True
            st[res_key] = results

        done = st.get(run_key)
        results = st.get(res_key)
        return done, results

    def OnTextMenuClick(self, _sender, _args):
        try:
            self.wait_for_completion = not self.wait_for_completion
            self.ExpireSolution(True)
        except Exception as ex:
            add_error(str(ex))

    def AppendAdditionalMenuItems(self, items):
        component.AppendAdditionalMenuItems(self, items)

        try:
            image = None
            item = items.Items.Add('Wait for completion', image, self.OnTextMenuClick)
            item.Checked = self.wait_for_completion
        except Exception as ex:
            add_error(str(ex))
