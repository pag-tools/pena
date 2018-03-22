import logging, sys
from random import Random,choice

from tname.core.model import Runner, Configuration


class Pairwise(Runner):
    def run(self, config):
        conflicts = set({})
        for i in range(len(config)):
            for j in range(i + 1, len(config)):
                pair = config.factory([config[i], config[j]])
                has_conflicts = self._verifier.is_conflicting(pair)
                logging.debug("{}({}) {}".format(("  " * (j - i)), has_conflicts, pair))
                if has_conflicts:
                    conflicts.add(pair)
        return conflicts


class SplitSearch(Runner):
    def __init__(self, verifier, iterative=True):
        super().__init__(verifier)
        self.__ITERATIVE = iterative
        self.__INITIAL_SEED = 12345
        self.__remaining_plugins = set({})
        self.limit_iteration = 20

    def run(self, config):
        logging.info("STEP - Started search")
        if not self._verifier.is_conflicting(config):
            logging.info("STEP - Finished search")
            return set({})

        self.__remaining_plugins.update(config[:])
        conflicts = self._search(config, shuffler=Random(self.__INITIAL_SEED))
        if not self.__ITERATIVE:
            logging.info("STEP - Finished search")
            return conflicts

        minimized = set({})
        self._iterative(conflicts, minimized)

        logging.info("STEP - Finished search")
        return minimized

    def _search(self, config, shuffler, retry=0, dep=0):
        conflicts = set({})
        has_conflicts = self._verifier.is_conflicting(config)
        logging.debug("{}({}) {}".format(("  " * dep), has_conflicts, config))
        if has_conflicts:
            if len(config) == 2 or (len(config) == 3 and self.limit_iteration == 0):
                self.limit_iteration = 20
                single_plugin = set({choice(config[:])})
                self.__remaining_plugins.difference_update(single_plugin)
                conflicts.add(config)
                return conflicts
                
            self.limit_iteration -= 1
            mid = len(config) >> 1
            left, right = config.factory(config[:mid]), config.factory(config[mid:])
            left_conflicts, right_conflicts = self._verifier.is_conflicting(left), self._verifier.is_conflicting(right)

            if left_conflicts and not right_conflicts:
                return self._search(left, shuffler, dep=dep + 1)
            elif not left_conflicts and right_conflicts:
                return self._search(right, shuffler, dep=dep + 1)
            elif left_conflicts and right_conflicts:
                return self._search(left, shuffler, dep=dep + 1).union(
                    self._search(right, shuffler, dep=dep + 1))
            elif retry > len(config) >> 1:
                conflicts.add(config)
                return conflicts
            else:
                shuffler.shuffle(config)
                return self._search(config, shuffler, dep=dep, retry=retry + 1)

        return conflicts

    def _iterative(self, conflicts, minimized, iteration=1):
        logging.debug(self.__remaining_plugins)
        for conflict in conflicts:
            if len(conflict) == 2:
                minimized.add(conflict)
            else:
                logging.info("Iterative run")
                seed = self.__INITIAL_SEED + iteration
                sub = self._search(conflict, Random(seed))
                self._iterative(sub, minimized, iteration + 1)

        c = Configuration(self.__remaining_plugins)
        if self._verifier.is_conflicting(c):
            logging.info("Iterative run")
            seed = self.__INITIAL_SEED + iteration
            sub = self._search(c, Random(seed))
            self._iterative(sub, minimized, iteration + 1)
