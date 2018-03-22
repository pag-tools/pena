import random
import unittest

from tname.core.model import Configuration, check_frequency


class TestConfiguration(unittest.TestCase):
    def test_reflexivity(self):
        self.assertEqual(Configuration(["plugin-A"]), Configuration(["plugin-A"]))

    def test_commutativity(self):
        plugins = ("plugin-A", "plugin-B", "plugin-C", "plugin-D")
        shuffler = random.Random(12345)
        for i in range(10):
            copy = [p for p in plugins]
            shuffler.shuffle(copy)
            self.assertEqual(Configuration(plugins), Configuration(copy))

        c = Configuration(plugins)
        other = Configuration(plugins)
        shuffler.shuffle(other)
        self.assertEqual(other, c)
        self.assertEqual(Configuration(["1", "3"]), Configuration(["3", "1"]))

    def test_immutability(self):
        plugins = ["plugin-A"]
        c = Configuration(plugins)
        plugins.pop()
        self.assertEqual(len(c), 1)
        self.assertFalse(len(plugins))

    def test_contains(self):
        self.assertTrue(Configuration(["plugin-A"]) in Configuration(("plugin-A", "plugin-B", "plugin-C", "plugin-D")))
        self.assertTrue(Configuration(["plugin-A"]) in Configuration(["plugin-A"]))
        configs = [
            Configuration(["plugin-A", "plugin-B", "plugin-C", "plugin-D"]),
            Configuration(["plugin-A", "plugin-B", "plugin-C"]),
            Configuration(["plugin-A", "plugin-B"])
        ]
        self.assertTrue(Configuration(["plugin-A", "plugin-B"]) in configs)
        [self.assertTrue(Configuration(["plugin-A"]) in c) for c in configs]

    def test_difference(self):
        c1 = Configuration(["plugin-A", "plugin-B", "plugin-C", "plugin-D"])
        c2 = Configuration(["plugin-A"])
        self.assertEqual(Configuration(["plugin-B", "plugin-C", "plugin-D"]), c1.difference(c2))


class TestCheckFrequency(unittest.TestCase):
    def setUp(self):
        self.empty = []
        self.disjoint_conflicts = {
            Configuration(["plugin-A", "plugin-B"]),
            Configuration(["plugin-D", "plugin-E"]),
        }
        self.conflicts = {
            Configuration(["plugin-A", "plugin-B"]),
            Configuration(["plugin-A", "plugin-D"]),
            Configuration(["plugin-B", "plugin-D"]),
            Configuration(["plugin-D", "plugin-E"]),
        }

    def test_no_conflicts(self):
        self.assertEqual({}, check_frequency(self.empty))

    def test_disjoint_conflicts(self):
        expected = {
            "plugin-A": 1,
            "plugin-B": 1,
            "plugin-D": 1,
            "plugin-E": 1
        }
        self.assertEqual(expected, check_frequency(self.disjoint_conflicts))

    def test_conflicts(self):
        expected = {
            "plugin-A": 2,
            "plugin-B": 2,
            "plugin-D": 3,
            "plugin-E": 1
        }
        self.assertEqual(expected, check_frequency(self.conflicts))

    def test_print(self):
        [print("{}: {}".format(k, v)) for k, v in check_frequency(self.disjoint_conflicts).items()]
        [print("{}: {}".format(k, v)) for k, v in check_frequency(self.empty).items()]
        [print("{}: {}".format(k, v)) for k, v in check_frequency(self.conflicts).items()]
