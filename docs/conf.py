# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme


project = 'Sphindexer Project'
copyright = '2021, @KoKekkoh, @Kakkouo'
author = 'Kakkouo'
release = '0.2.0'


extensions = [
    'sphindexer',
    'sphinxcontrib.actdiag',
    'sphinxcontrib.seqdiag',
    #'sphinxcontrib.blockdiag',
    #'sphinxcontrib.nwdiag',
    #'sphinxcontrib.rackdiag',
    ]


templates_path = ['_templates']
language = 'en'
exclude_patterns = []


html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['.static', ]
html_favicon = '.static/favicon.ico'
