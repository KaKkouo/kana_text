#!/usr/bin/python
import sys
import pytest

from src import ExtSubterm as sb, KanaText as kt

testcase01i = [
    sb('5', kt('似似'), kt('参参')),
    sb('5', kt('似似'), kt('')),
    sb('5', kt(''), kt('参参')),
    sb('5', kt(''), kt('')),
]

testcase01o = [
    "<ExtSubterm: len=2 <KanaText: len=1 <#text: '似似'>><KanaText: len=1 <#text: '参参'>>>",
    "<ExtSubterm: len=1 <KanaText: len=1 <#text: '似似'>>>",
    "<ExtSubterm: len=1 <KanaText: len=1 <#text: '参参'>>>",
    "<ExtSubterm: len=0 >",
    ]


def test01_repr():
    for t, e in zip(testcase01i, testcase01o):
        assert repr(t) == e
