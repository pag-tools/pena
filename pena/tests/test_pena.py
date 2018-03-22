import os

from unittest import TestCase

from tname.core.pena import PENA
from tname.core.cms import WordPressCLI


CLI = WordPressCLI(home=os.path.join("environment", "wordpress", "wordpress"))

class TestPena(TestCase):
    pass