# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://pydata-sphinx-theme.readthedocs.io

# -- Path setup --------------------------------------------------------------

import os, shutil, sys

sys.path.append(os.path.abspath("../../src/entrainment/"))

# -- Fixes and Tweaks ---------------------------------------------------------

shutil.copyfile("../../README.md", "index.md")

delete = [""]

for i in delete:
    for j in os.listdir():
        if os.path.isfile(j):
            con = open(j, "rt")
            data = con.read()
            data = data.replace(i, "")
            con.close()
            
            con = open(j, "wt")
            con.write(data)
            con.close()

# -- Project information -----------------------------------------------------

# import entrainment
import sphinx_bootstrap_theme

project = 'entrainment'
copyright = '2023, Daniel Vartanian'
author = 'Daniel Vartanian'
version = "0.0.0.9000"
# version = entrainment.__version__ # The short X.Y version.
# release = "" # The full version, including alpha/beta/rc tags.

# -- General configuration ---------------------------------------------------

# Don't forget to update the `requirements.txt` with the pakages extensions.

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    'sphinx.ext.intersphinx',
    "sphinx_copybutton",
    "sphinx_design",
]

def setup(app):
    app.add_css_file("custom.css")

source_suffix = [".rst", ".md"]

# Enable todo output
todo_include_todos = True

# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"

# -- Sitemap -------------------------------------------------------------

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Extension options -------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence", "substitution"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
html_theme = "bootstrap" # "alabaster"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a
# theme further.
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_title': "entrainment",

    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "",

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    'navbar_links': [
        ("Reference", "reference"),
        ("Latitude hypothesis", "hypothesis-test"),
        ("Contributing", "contributing"),
        ("Changelog", "changelog"),
    ],

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 2,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "false",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    'navbar_class': "navbar",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': "true",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "",

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "cosmo",

    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    'bootstrap_version': "3",
}

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    "index": ["localtoc.htmlv],
    "reference": ["localtoc.htmlv],
    "hypothesis-test": ["localtoc.htmlv],
    "contributing": ["localtoc.htmlv],
    "changelog": ["localtoc.htmlv],
    }

myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

html_context = {
    "default_mode": "auto",
    "github_user": "danielvartan",
    "github_repo": "entrainment",
    "github_version": "main",
    "doc_path": "docs",
}

# (Optional) Logo. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
# html_logo = "my_logo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'
