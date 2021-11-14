#!/usr/bin/python
import sys
import pytest

from src import ExtIndexUnit as IndexUnit, ExtSubterm as sb, KanaText as kt

testcase01i = [
    (kt('壱壱'), sb('5', kt('似似'), kt('参参')),'2' , '5', 'doc1', 'id-01', '分類子'),
    (kt('壱壱'), sb('5', kt('似似'), kt('')),'2' , '5', 'doc1', 'id-01', '分類子'),
    (kt('壱壱'), sb('5', kt(''), kt('')),'2' , '5', 'doc1', 'id-01', '分類子'),
    (kt('壱壱'), sb('5', kt('似似'), kt('参参')),'2' , '5', '', '', ''),
    (kt('壱壱'), sb('5', kt('似似'), kt('')),'2' , '5', '', '', ''),
    (kt('壱壱'), sb('5', kt(''), kt('')),'2' , '5', '', '', ''),
    (kt('いい|壱壱'), sb('5', kt(''), kt('')),'2' , '5', '', '', ''),
    (kt('いい|壱壱^'), sb('5', kt(''), kt('')),'2' , '5', '', '', ''),
    (kt('いい|壱壱^11'), sb('5', kt(''), kt('')),'2' , '5', '', '', ''),
]

testcase01o = [
    "<ExtIndexUnit: main file_name='doc1' target='id-01' <#text: ''><KanaText: len=1 <#text: '壱壱'>><ExtSubterm: len=2 <KanaText: len=1 <#text: '似似'>><KanaText: len=1 <#text: '参参'>>>>",
    "<ExtIndexUnit: main file_name='doc1' target='id-01' <#text: ''><KanaText: len=1 <#text: '壱壱'>><ExtSubterm: len=1 <KanaText: len=1 <#text: '似似'>>>>",
    "<ExtIndexUnit: main file_name='doc1' target='id-01' <#text: ''><KanaText: len=1 <#text: '壱壱'>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=1 <#text: '壱壱'>><ExtSubterm: len=2 <KanaText: len=1 <#text: '似似'>><KanaText: len=1 <#text: '参参'>>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=1 <#text: '壱壱'>><ExtSubterm: len=1 <KanaText: len=1 <#text: '似似'>>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=1 <#text: '壱壱'>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=2 <#text: 'いい|壱壱'>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=2 ruby='on' <#text: 'いい|壱壱'>>>",
    "<ExtIndexUnit: main <#text: ''><KanaText: len=2 ruby='specific' option='11' <#text: 'いい|壱壱'>>>",
    ]

#__getitem__
testcase02i = (
    kt('いい|壱壱^11'), sb('5', kt('ろろ|弐弐^'), kt('はは|参参^2')),
    3, 4, 'doc1', 'id-02', '分類子')

testcase02o = [
    4, 'doc1', 'id-02', '分類子',
    "<#text: ''>",
    "<KanaText: len=2 ruby='specific' option='11' <#text: 'いい|壱壱'>>",
    "<ExtSubterm: len=2 <KanaText: len=2 ruby='on' <#text: 'ろろ|弐弐'>><KanaText: len=2 ruby='specific' option='2' <#text: 'はは|参参'>>>",
]


def test01_repr():
    for t, e in zip(testcase01i, testcase01o):
        iu = IndexUnit(*t)
        rslt = repr(iu)
        assert rslt == e

def test02_getitem():
    iu = IndexUnit(*testcase02i)
    assert testcase02o[0] == iu['main']
    assert testcase02o[1] == iu['file_name']
    assert testcase02o[2] == iu['target']
    assert testcase02o[3] == iu['index_key']
    assert testcase02o[4] == repr(iu[0])
    assert testcase02o[5] == repr(iu[1])
    assert testcase02o[6] == repr(iu[2])
