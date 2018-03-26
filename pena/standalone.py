#!/usr/bin/env python3
import logging, time, sys, random, ast

from tname.core.execution import Pairwise, SplitSearch
from tname.core.pena import PENA
from experiments.setup import setup

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
    datefmt="%I:%M:%S %p",
    filename="/pena/standalone.log"
)

pena = PENA(cms_path="/var/www/html")

### update settings ###
pena.set_mode(SplitSearch)
pena.set_skip_dimensionality(True)
pena.visual_oracle = False
pena.remove_spurious = True

### add plugins###
PLUGINS = []
pena.set_input_plugins(PLUGINS)
pena.run()
