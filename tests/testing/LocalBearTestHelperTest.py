from queue import Queue
import unittest

from tests.test_bears.TestBear import TestBear
from tests.test_bears.TestBearDep import (TestDepBearBDependsA,
                                          TestDepBearCDependsB,
                                          TestDepBearDependsAAndAA)
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper as Helper


files = ('Everything is invalid/valid/raises error',)
invalidTest = verify_local_bear(TestBear,
                                valid_files=(),
                                invalid_files=files,
                                settings={'result': True})
validTest = verify_local_bear(TestBear,
                              valid_files=files,
                              invalid_files=())


class LocalBearCheckResultsTest(Helper):

    def setUp(self):
        section = Section('')
        section.append(Setting('result', 'a, b'))
        self.uut = TestBear(section, Queue())

    def test_order_ignored(self):
        self.check_results(self.uut, ['a', 'b'], ['b', 'a'],
                           check_order=False)

    def test_require_order(self):
        with self.assertRaises(AssertionError):
            self.check_results(self.uut, ['a', 'b'], ['b', 'a'],
                               check_order=True)


class LocalBearTestCheckLineResultCountTest(Helper):

    def setUp(self):
        section = Section('')
        section.append(Setting('result', True))
        self.uut = TestBear(section, Queue())

    def test_check_line_result_count(self):
        self.check_line_result_count(self.uut,
                                     ['a', '', 'b', '   ', '# abc', '1'],
                                     [1, 1, 1])


class LocalBearTestDependency(Helper):

    def setUp(self):
        self.section = Section('')

    def test_check_results_bear_with_dependency(self):
        bear = TestDepBearBDependsA(self.section, Queue())
        self.check_results(bear, [], [['settings1',
                                       'settings2',
                                       'settings3',
                                       'settings4']],
                           settings={'settings1': 'settings1',
                                     'settings2': 'settings2',
                                     'settings3': 'settings3',
                                     'settings4': 'settings4'})

    def test_check_results_bear_with_2_deep_dependency(self):
        bear = TestDepBearCDependsB(self.section, Queue())
        self.check_results(bear, [], [['settings1',
                                       'settings2',
                                       'settings3',
                                       'settings4',
                                       'settings5',
                                       'settings6']],
                           settings={'settings1': 'settings1',
                                     'settings2': 'settings2',
                                     'settings3': 'settings3',
                                     'settings4': 'settings4',
                                     'settings5': 'settings5',
                                     'settings6': 'settings6'})

    def test_check_results_bear_with_two_dependencies(self):
        bear = TestDepBearDependsAAndAA(self.section, Queue())
        self.check_results(bear, [], [['settings1',
                                       'settings2',
                                       'settings3',
                                       'settings4']],
                           settings={'settings1': 'settings1',
                                     'settings2': 'settings2',
                                     'settings3': 'settings3',
                                     'settings4': 'settings4'})


class LocalBearTestHelper(unittest.TestCase):

    def setUp(self):
        section = Section('')
        section.append(Setting('exception', True))
        self.uut = TestBear(section, Queue())

    def test_exception(self):

        with self.assertRaises(AssertionError), execute_bear(
                self.uut,  'Luke', files[0]) as result:
            pass
