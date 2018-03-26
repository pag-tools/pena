from random import randrange, Random
from .black_list import BLACK_LIST

def get_plugins():
    """
    Description:
        Get all plugins 
    Params:
        None
    Return:
        List of plugins
    """
    with open('./experiments/plugins') as f:
        _list = f.read().split('\n')
        plugins = [plugin.strip() for plugin in _list if plugin]
    return plugins

def randomize_plugins(plugins):
    seeds = [98765432, 12345, 99999, 54321, 56789]
    Random(randrange(len(seeds))).shuffle(plugins)
    return plugins

def setup(size, preconfig=[], ignore=[]):
    """
    Description:
        Generate list of plugins according a size input
    Params:
        size: list length
    Optional Params:
        preconfig: list of plugins that will be inserted before plugin selection
        ignore: list of plugins that will be ignored during plugin selection
    Return:
        List of plugins
    """
    plugins = get_plugins()
    preconfig = preconfig[:]
    skip_plugins = BLACK_LIST + ignore + preconfig
    while len(preconfig) < size:
        r = randrange(len(plugins))
        candidate = plugins[r]
        if (candidate not in skip_plugins) and (candidate not in preconfig):
            preconfig.append(candidate)
    return preconfig

