#!/usr/bin/python
import sys
import pytest

from src import KanaText

def test01_empty():
    term = KanaText('')
    assert repr(term) == "<#text: ''>"
    assert term['kana'] == None
    assert term['hier'] == ""

def test02_raise():
    term = KanaText('用語零弐')
    with pytest.raises(IndexError):
        text = term[2]
    with pytest.raises(TypeError):
        text = term[(1, 1)]
    with pytest.raises(AttributeError):
        term[3] = "よみ"
    with pytest.raises(TypeError):
        term[(1, 1)] = "よみ"

def test02_repr():
    term = KanaText("", "用語零参")
    assert repr(term) == "<#rawtext: '用語零参'>"
