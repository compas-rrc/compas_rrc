# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import m2r2
import sphinx_compas_theme
from sphinx.ext.napoleon.docstring import NumpyDocstring

# patches

current_m2r2_setup = m2r2.setup


def patched_m2r2_setup(app):
    try:
        return current_m2r2_setup(app)
    except (AttributeError):
        app.add_source_suffix(".md", "markdown")
        app.add_source_parser(m2r2.M2RParser)
    return dict(
        version=m2r2.__version__,
        parallel_read_safe=True,
        parallel_write_safe=True,
    )


m2r2.setup = patched_m2r2_setup
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "m2r2",
]
if os.getenv("SPELLCHECK"):
    extensions += ("sphinxcontrib.spelling",)
    spelling_show_suggestions = True
    spelling_lang = "en_US"

source_suffix = ".rst"
master_doc = "index"
project = "COMPAS RRC"
year = "2019"
author = "ETH Zurich"
copyright = "{0}, {1}".format(year, author)
version = release = "1.1.0"

pygments_style = "sphinx"
show_authors = True
add_module_names = True
templates_path = [
    "_templates",
]
extlinks = {
    "issue": ("https://github.com/compas-rrc/compas_rrc/issues/%s", "#"),
    "pr": ("https://github.com/compas-rrc/compas_rrc/pull/%s", "PR #"),
}

# intersphinx options
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "compas": ("https://compas.dev/compas/latest/", None),
    "compas_fab": ("https://gramaziokohler.github.io/compas_fab/latest/", None),
    "roslibpy": ("https://roslibpy.readthedocs.io/en/latest/", None),
}

# autodoc options
autodoc_default_options = {
    "member-order": "bysource",
    "exclude-members": "__weakref__",
    "undoc-members": True,
    "private-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "alphabetical"

# autosummary options
autosummary_generate = True

# collect doc versions
package_docs_root = "https://compas-rrc.github.io/compas_rrc/"

with open(os.path.join(os.path.dirname(__file__), "doc_versions.txt"), "r") as f:
    version_names = [version.strip() for version in f.readlines()]
    package_docs_versions = [
        (version, "{}{}/".format(package_docs_root, version)) for version in version_names if version
    ]

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"
html_theme = "compaspkg"
html_theme_path = sphinx_compas_theme.get_html_theme_path()
html_theme_options = {
    "package_name": "compas_rrc",
    "package_title": project,
    "package_version": release,
    "package_repo": "https://github.com/compas-rrc/compas_rrc",
    "package_docs": package_docs_root,
    "package_old_versions": package_docs_versions,
}

html_split_index = False
html_short_title = "%s-%s" % (project, version)
html_context = {}
html_static_path = ["_static"]
html_last_updated_fmt = "%b %d, %Y"
html_copy_source = False
html_show_sourcelink = False
html_permalinks = False
html_permalinks_icon = ""
html_experimental_html5_writer = True
html_compact_lists = True

# napoleon options
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

# Parse Attributes and Class Attributes on Class docs same as parameters.
# first, we define new methods for any new sections and add them to the class


def parse_keys_section(self, section):
    return self._format_fields("Keys", self._consume_fields())


NumpyDocstring._parse_keys_section = parse_keys_section


def parse_attributes_section(self, section):
    return self._format_fields("Attributes", self._consume_fields())


NumpyDocstring._parse_attributes_section = parse_attributes_section


def parse_class_attributes_section(self, section):
    return self._format_fields("Class Attributes", self._consume_fields())


NumpyDocstring._parse_class_attributes_section = parse_class_attributes_section


# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections["keys"] = self._parse_keys_section
    self._sections["class attributes"] = self._parse_class_attributes_section
    self._unpatched_parse()


NumpyDocstring._unpatched_parse = NumpyDocstring._parse
NumpyDocstring._parse = patched_parse
