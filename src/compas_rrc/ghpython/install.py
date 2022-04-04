import glob
import os

import compas.plugins
import compas_ghpython.components


@compas.plugins.plugin(category='install')
def after_rhino_install(installed_packages):
    if 'compas_rrc' not in installed_packages:
        return []

    src = os.path.join(os.path.dirname(__file__), 'components', 'ghuser')
    installed_objects = compas_ghpython.components.install_userobjects(src)

    return [('compas_rrc', 'Installed {} GH User Objects'.format(len(installed_objects)), True)]


@compas.plugins.plugin(category='install')
def after_rhino_uninstall(uninstalled_packages):
    if 'compas_rrc' not in uninstalled_packages:
        return []

    srcdir = os.path.join(os.path.dirname(__file__), 'components', 'ghuser')
    userobjects = [os.path.basename(ghuser) for ghuser in glob.glob(os.path.join(srcdir, '*.ghuser'))]
    uninstalled_objects = compas_ghpython.components.uninstall_userobjects(userobjects)

    uninstall_errors = [uo[0] for uo in uninstalled_objects if not uo[1]]
    error_msg = '' if not uninstall_errors else 'and {} failed to uninstall'.format(len(uninstall_errors))

    return [('compas_rrc', 'Uninstalled {} GH User Objects {}'.format(len(uninstalled_objects), error_msg), True)]
