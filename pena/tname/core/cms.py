import os, subprocess
from subprocess import check_output, call, DEVNULL

from tname.core.model import CMSInterface


class WordPressCLI(CMSInterface):
    def __init__(self, home):
        if not os.path.exists(home):
            raise IOError("Path  \"{}\" does not exist".format(home))
        self.__home = home
        self.__plugins = self.__fetch_plugins()

    def plugins(self):
        return self.__plugins

    def activate(self, plugins):
        """ activate a list of plugins """
        if len(plugins):
            cmd = ["wp", "plugin", "activate"]
            cmd.extend(plugins)
            cmd.append("--path={}".format(self.__home))
            call(cmd, stdout=DEVNULL, stderr=DEVNULL)

    def deactivate(self, plugins):
        """ deactivate a list of plugins """
        if len(plugins):
            cmd = ["wp", "plugin", "deactivate"]
            cmd.extend(plugins)
            cmd.append("--path={}".format(self.__home))
            call(cmd, stdout=DEVNULL, stderr=DEVNULL)

    def __fetch_plugins(self):
        """ fetch installed plugins as csv file """
        output = check_output(["wp", "plugin", "list", "--format=csv", "--field=name",
                               "--path={}".format(self.__home)])
        return {plugin for plugin in output.decode().splitlines()}
