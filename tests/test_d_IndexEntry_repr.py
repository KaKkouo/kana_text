#!/usr/bin/python
import sys
import pytest

from src import ExtIndexEntry as IndexEntry


def test01_repr():
    entry = IndexEntry("sphinx; python; docutils", "triple", "doc1", "id-111", "main")
    assert repr(entry) == "<ExtIndexEntry: entry_type='triple' main='main' " \
                          "file_name='doc1' target='id-111' " \
                          "<KanaText: len=1 <#text: 'sphinx'>>" \
                          "<KanaText: len=1 <#text: 'python'>>" \
                          "<KanaText: len=1 <#text: 'docutils'>>>"
