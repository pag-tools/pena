#!/usr/bin/env python3
import logging, time, sys
sys.path.append('../../')
from random import Random
from tname.core import runner
from tname.core.execution import Pairwise, SplitSearch
from experiments.setup import setup

args = sys.argv
file_name = args[1]
seed_value = int(args[2])

mode = Pairwise if str(file_name) == 'PW' else SplitSearch
log_name = 'A' if seed_value == 0 else 'B'

SEEDS = [
    8765432, 234323, 123456,
    98765, 857382, 6456453,
    24681098, 938291929, 768594,
    3214322
]

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
        datefmt="%I:%M:%S %p %j",
        filename="execution-seed{}-{}.log".format(log_name, str(file_name))
    )
    N = [x for x in range(10, 101, 10)]
    N.extend([150, 200])
    seed = SEEDS[seed_value]

    for n in N:
        rand = Random(seed)
        plugins = setup(k=n, rand=rand)
        rand.shuffle(plugins)

        logging.debug("RUNNING N={}".format(n))
        logging.debug("PLUGINS={}".format(plugins))
        logging.debug("SEED={}".format(seed))

        runner.run(
            input_plugins=plugins,
            mode=mode,
            cms_path="../../environment/wordpress/wordpress",
            url="http://localhost:8081"
        )
