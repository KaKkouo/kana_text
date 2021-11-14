import unittest

from . import testcase21, testcase22, testcase31
from . import testcase41, testcase42, testcase43, testcase61, testcase71
from . import testcase81, testcase82, testcase91, testcase92, testcase99

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testcase21.testIndexEntry))
    suites.addTests(unittest.makeSuite(testcase22.testIndexEntry))
    suites.addTests(unittest.makeSuite(testcase31.testIndexUnit))
    suites.addTests(unittest.makeSuite(testcase41.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase42.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase43.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase61.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase71.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase81.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase82.testIndexRack))
    #suites.addTests(unittest.makeSuite(testcase91.testIndexEntries))
    #suites.addTests(unittest.makeSuite(testcase92.testBuilder))
    #suites.addTests(unittest.makeSuite(testcase99.testCommand))
    return suites
