import unittest

from tname.core import execution
from tname.core.model import Configuration, Verifier


class MockVerifier(Verifier):
    def __init__(self):
        super().__init__(cms_cli=None, web_driver=None, heuristic=None)

    def is_conflicting(self, config):
        for p in {Configuration(["1", "2"]), Configuration(["3", "5"])}:
            if p in config:
                return True
        return False


class TestPairwise(unittest.TestCase):
    def test_run(self):
        config = Configuration(["1", "2", "3", "4", "5"])
        expected = {Configuration(["1", "2"]), Configuration(["3", "5"])}
        mode = execution.Pairwise(MockVerifier())
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_no_conflict(self):
        config = Configuration(["1", "3", "4"])
        expected = set({})
        mode = execution.Pairwise(MockVerifier())
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_single_pair(self):
        config = Configuration(["1", "2"])
        expected = {config}
        mode = execution.Pairwise(MockVerifier())
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)


class TestSplitSearch(unittest.TestCase):
    def test_single_pair(self):
        config = Configuration(["1", "2"])
        expected = {config}
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_no_conflict(self):
        config = Configuration(["1", "3"])
        expected = set({})
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_split_case1(self):
        config = Configuration(["1", "2", "3", "4"])
        expected = {Configuration(["1", "2"])}
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

        config = Configuration(["1", "2", "3", "5", "9", "10", "11", "12"])
        expected = {Configuration(["1", "2"]), Configuration(["3", "5"])}
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_split_case2(self):
        config = Configuration(["2", "4", "3", "5"])
        expected = {Configuration(["3", "5"])}
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_split_case3(self):
        config = Configuration(["1", "2", "3", "5"])
        expected = {Configuration(["3", "5"]), Configuration(["1", "2"])}
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_single_run(self):
        config = Configuration(["1", "2", "3", "4", "5"])
        expected = {Configuration(["1", "2"]), Configuration(["3", "4", "5"])}
        mode = execution.SplitSearch(MockVerifier(), iterative=False)
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)

    def test_iterative(self):
        config = Configuration(["1", "2", "3", "4", "5"])
        expected = {Configuration(["1", "2"]), Configuration(["3", "5"])}
        mode = execution.SplitSearch(MockVerifier())
        conflicts = mode.run(config)
        self.assertEqual(expected, conflicts)
