#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import IndexUnit, KanaText

testcase01i = [
    ('壱壱', '似似', '参参', '5', 'doc1', 'id-01', '分類子', KanaText),
    ('壱壱', '似似', '', '5', 'doc1', 'id-01', '分類子', KanaText),
    ('壱壱', '', '', '5', 'doc1', 'id-01', '分類子', KanaText),
    ('壱壱', '似似', '参参', '5', '', '', '', KanaText),
    ('壱壱', '似似', '', '5', '', '', '', KanaText),
    ('壱壱', '', '', '5', '', '', '', KanaText),
    ('いい|壱壱', '', '', '5', '', '', '', KanaText),
    ('いい|壱壱^', '', '', '5', '', '', '', KanaText),
    ('いい|壱壱^11', '', '', '5', '', '', '', KanaText),
]

testcase01o = [
    "<IndexUnit: main='5' file_name='doc1' target='id-01' <KanaText: <#empty>><KanaText: <#text: '壱壱'>><SubTerm: <KanaText: <#text: '似似'>><KanaText: <#text: '参参'>>>>",
    "<IndexUnit: main='5' file_name='doc1' target='id-01' <KanaText: <#empty>><KanaText: <#text: '壱壱'>><SubTerm: <KanaText: <#text: '似似'>>>>",
    "<IndexUnit: main='5' file_name='doc1' target='id-01' <KanaText: <#empty>><KanaText: <#text: '壱壱'>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: <#text: '壱壱'>><SubTerm: <KanaText: <#text: '似似'>><KanaText: <#text: '参参'>>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: <#text: '壱壱'>><SubTerm: <KanaText: <#text: '似似'>>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: <#text: '壱壱'>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: <#text: 'いい|壱壱'>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: ruby='on' <#text: 'いい|壱壱'>>>",
    "<IndexUnit: main='5' <KanaText: <#empty>><KanaText: ruby='specific' option='11' <#text: 'いい|壱壱'>>>",
    ]

#__getitem__
testcase02i = (
    'いい|壱壱^11', 'ろろ|弐弐^', 'はは|参参^2',
    '5', 'doc1', 'id-02', '分類子', KanaText)

testcase02o = [
    '5', 'doc1', 'id-02', '分類子',
    "<KanaText: <#empty>>",
    "<KanaText: ruby='specific' option='11' <#text: 'いい|壱壱'>>",
    "<SubTerm: <KanaText: ruby='on' <#text: 'ろろ|弐弐'>><KanaText: ruby='specific' option='2' <#text: 'はは|参参'>>>",
    "'5'",
]


class testIndexUnit(unittest.TestCase):
    #repr
    def test01_repr(self):
        for t, e in zip(testcase01i, testcase01o):
            iu = IndexUnit(*t)
            rslt = repr(iu)
            self.assertEqual(e, rslt)

    def test02_getitem(self):
        iu = IndexUnit(*testcase02i)
        self.assertEqual(testcase02o[0], iu['main'])
        self.assertEqual(testcase02o[1], iu['file_name'])
        self.assertEqual(testcase02o[2], iu['target'])
        self.assertEqual(testcase02o[3], iu['index_key'])
        self.assertEqual(testcase02o[4], repr(iu[0]))
        self.assertEqual(testcase02o[5], repr(iu[1]))
        self.assertEqual(testcase02o[6], repr(iu[2]))
        self.assertEqual(testcase02o[7], repr(iu[3]))

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
