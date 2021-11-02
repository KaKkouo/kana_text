import unittest

from . import testcase01, testcase02, testcase03, testcase04, testcase05
from . import testcase06, testcase07, testcase08
from . import testcase11, testcase12, testcase13
from . import testcase21, testcase22, testcase31
from . import testcase41, testcase42, testcase43, testcase61, testcase71
from . import testcase81, testcase82, testcase91, testcase92, testcase99

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testcase01.testKanaText))
    suites.addTests(unittest.makeSuite(testcase02.testKanaText))
    suites.addTests(unittest.makeSuite(testcase03.testKanaText))
    suites.addTests(unittest.makeSuite(testcase04.testKanaText))
    suites.addTests(unittest.makeSuite(testcase05.testKanaText))
    suites.addTests(unittest.makeSuite(testcase06.testKanaText))
    suites.addTests(unittest.makeSuite(testcase07.testKanaText))
    suites.addTests(unittest.makeSuite(testcase08.testKanaText))
    suites.addTests(unittest.makeSuite(testcase11.testKanaText))
    suites.addTests(unittest.makeSuite(testcase12.testKanaText))
    suites.addTests(unittest.makeSuite(testcase13.testKanaText))
    suites.addTests(unittest.makeSuite(testcase21.testIndexEntry))
    suites.addTests(unittest.makeSuite(testcase22.testIndexEntry))
    suites.addTests(unittest.makeSuite(testcase31.testIndexUnit))
    suites.addTests(unittest.makeSuite(testcase41.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase42.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase43.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase61.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase71.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase81.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase82.testIndexRack))
    suites.addTests(unittest.makeSuite(testcase91.testIndexEntries))
    suites.addTests(unittest.makeSuite(testcase92.testBuilder))
    suites.addTests(unittest.makeSuite(testcase99.testCommand))
    return suites
