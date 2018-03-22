#!/usr/bin/env python3
import logging

from tname.core.execution import Pairwise, SplitSearch
from tname.core.pena import PENA
from experiments.setup import setup

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
    datefmt="%I:%M:%S %p",
    filename="logs/standalone.log"
)

pena = PENA(cms_path="./environment/wordpress/wordpress")

### update settings ###
pena.set_mode(SplitSearch)
pena.set_skip_dimensionality(True)
pena.visual_oracle = True
pena.remove_spurious = True

### add plugins###
PLUGINS = setup(k=100) # get 100 plugins from dataset
pena.set_input_plugins(PLUGINS)
pena.run()