#!/usr/bin/bash -x

readonly LIST="py36 py37 py38 py39"

for v in $LIST
do
	.tox/${v}/bin/python -m pip install --upgrade pip Sphinx pytest pytest-cov sphindexer
done

