#!/usr/bin/python
import sys
import unittest

from src import ExIndexEntry as IndexEntry


class testIndexEntry(unittest.TestCase):
    def test01_repr(self):
        entry = IndexEntry("sphinx; python; docutils", "triple", "doc1", "id-111", "main")
        self.assertEqual(repr(entry),
                         "<ExIndexEntry: entry_type='triple' main='main' " \
                         "file_name='doc1' target='id-111' " \
                         "<KanaText: len=1 <#text: 'sphinx'>>" \
                         "<KanaText: len=1 <#text: 'python'>>" \
                         "<KanaText: len=1 <#text: 'docutils'>>>")


if __name__ == '__main__':
    unittest.main()
