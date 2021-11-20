#!/usr/bin/python
import sys
import pytest

from src import ExtIndexEntry as IndexEntry


def test01_repr():
    entry = IndexEntry("sphinx; python; docutils", "triple", "doc1", "id-111", "main")
    assert repr(entry) == "<ExtIndexEntry: entry_type='triple' main " \
                          "file_name='doc1' target='id-111' " \
                          "<KanaText: len=1 <#text: 'sphinx'>>" \
                          "<KanaText: len=1 <#text: 'python'>>" \
                          "<KanaText: len=1 <#text: 'docutils'>>>"

def test02_repr():
    entry = IndexEntry("sphinx; python; docutils; learning sphinx",
                       "keys", "doc1", "id-211", "main")
    assert repr(entry) == "<ExtIndexEntry: entry_type='keys' main " \
                          "file_name='doc1' target='id-211' " \
                          "<KanaText: len=1 <#text: 'sphinx'>>" \
                          "<KanaText: len=1 <#text: 'python'>>" \
                          "<KanaText: len=1 <#text: 'docutils'>>" \
                          "<KanaText: len=1 <#text: 'learning sphinx'>>>"

def test03_repr():
    entry = IndexEntry("sphinx; python; docutils", "pairs", "doc1", "id-311", "main")
    assert repr(entry) == "<ExtIndexEntry: entry_type='pairs' main " \
                          "file_name='doc1' target='id-311' " \
                          "<KanaText: len=1 <#text: 'sphinx'>>" \
                          "<KanaText: len=1 <#text: 'python'>>" \
                          "<KanaText: len=1 <#text: 'docutils'>>>"
