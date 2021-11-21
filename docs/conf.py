# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme


project = 'Sphinx Kana Text Project'
copyright = '2021, @KoKekkoh, @Kakkouo'
author = 'Kakkouo'
release = '0.1.0'


extensions = [
    #'sphinxcontrib.kana_text',
    ]


templates_path = ['_templates']
language = 'ja'
exclude_patterns = []


html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['.static', ]
html_favicon = '.static/favicon.ico'
