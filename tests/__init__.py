import unittest

from . import testcase01, testcase02, testcase03, testcase04, testcase05
from . import testcase06, testcase07, testcase08, testcase09

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testcase01.testKanaText))
    suites.addTests(unittest.makeSuite(testcase02.testKanaTextUnit))
    suites.addTests(unittest.makeSuite(testcase03.testIndexUnit))
    suites.addTests(unittest.makeSuite(testcase04.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase05.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase06.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase07.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase08.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase09.testIndexEntries))
    return suites
