import os
from unittest import TestCase
from unittest import skip

from tname.core.cms import WordPressCLI

CLI = WordPressCLI(home=os.path.join("environment", "wordpress", "wordpress"))


class TestWordPressCLI(TestCase):
    @skip("Expected plugins may change")
    def test_plugins(self):
        expected_plugins = {"hello", "akismet"}
        self.assertEqual(expected_plugins, CLI.plugins())

    def test_active_deactivate(self):
        # Dummy test. Just ensuring test runs and no crash occurs.
        CLI.activate(["hello"])
        CLI.deactivate(["hello"])
