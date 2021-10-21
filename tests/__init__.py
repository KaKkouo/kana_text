import unittest

from . import testcase01, testcase21, testcase31
from . import testcase41, testcase43, testcase61, testcase71
from . import testcase81, testcase91

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testcase01.testKanaText))
    suites.addTests(unittest.makeSuite(testcase21.testKanaTextUnit))
    suites.addTests(unittest.makeSuite(testcase31.testIndexUnit))
    suites.addTests(unittest.makeSuite(testcase41.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase43.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase61.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase71.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase81.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase91.testIndexEntries))
    return suites
