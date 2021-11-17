#!/usr/bin/python
import os, pytest
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

#-------------------------------------------------------------------

inliner = Inliner()

workdir = 'tests'
distdir = workdir + '/out'
htmfile = distdir + '/index.html'

#-------------------------------------------------------------------

def test01_build():
    try:
        os.remove(htmfile)
    except FileNotFoundError:
        pass

    application = Sphinx(workdir, workdir, distdir, distdir, "kana")
    bld = application.builder

    with pytest.raises(AttributeError):
        bld.write_genindex()

    application.build(False, ['tests/index.rst'])
    bld.config.html_split_index = True

    with pytest.raises(TypeError):
        bld.write_genindex()
