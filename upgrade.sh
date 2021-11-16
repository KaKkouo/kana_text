#!/usr/bin/bash -x

.tox/py36/bin/python -m pip install --upgrade pytest sphindexer
.tox/py37/bin/python -m pip install --upgrade pytest sphindexer
.tox/py38/bin/python -m pip install --upgrade pytest sphindexer

