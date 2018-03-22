import difflib
import hashlib
import logging
import os
import shutil
import tempfile
import urllib.request
from collections import OrderedDict

from bs4 import BeautifulSoup
import time
from tname.core.timer import Timer


class Verifier:
    """ Entity that knows how to check if conflicts exist. """

    def __init__(self, cms_cli, web_driver, heuristic):
        self.__cms_cli = cms_cli
        self.__web_driver = web_driver
        self.__delta_cache = {}
        self.__conflict_cache = {}
        self.__fn = heuristic
        self.__conflicting_changes = {}

    def is_conflicting(self, config):
        logging.info("STEP - Started checking")
        if len(config) < 2:
            logging.info("STEP - checking finished len(config) < 2")
            return False

        if config in self.__conflict_cache.keys():
            logging.info("STEP - checking finished (cache hit!)")
            return self.__conflict_cache[config]

        plugins_off_doc = self.__web_driver.html_document_path("none")

        delta_single_plugins = set({})
        for plugin in config:
            if plugin in self.__delta_cache.keys():
                delta_single_plugins.update(self.__delta_cache[plugin])
            else:
                plugin_doc = self.__web_driver.html_document_path(plugin)
                self.__delta_cache[plugin] = self.__delta(plugins_off_doc, plugin_doc)
                delta_single_plugins.update(self.__delta_cache[plugin])

        t_init_delta = time.time()
        self.__cms_cli.activate(config)
        html_all = self.__web_driver.fetch()
        self.__web_driver.save(html_all, "all")
        plugins_all_doc = self.__web_driver.html_document_path("all")
        self.__cms_cli.deactivate(config)
        Timer.update_delta(time.time() - t_init_delta)

        delta_all_plugins = self.__delta(plugins_off_doc, plugins_all_doc)
        is_preserved = (delta_single_plugins == delta_all_plugins)
        if not is_preserved:
            unexpected_added = delta_all_plugins.difference(delta_single_plugins)
            unexpected_removed = delta_single_plugins.difference(delta_all_plugins)
            self.__conflicting_changes[config] = (unexpected_added, unexpected_removed)
        
        self.__conflict_cache[config] = not is_preserved

        logging.info("STEP - checking finished")
        return not is_preserved

    def conflicting_changes(self, config):
        return self.__conflicting_changes[config]

    def update_changes(self, config, unexpected_added, unexpected_removed):
        self.__conflicting_changes[config] = (unexpected_added, unexpected_removed)

    def __delta(self, doc_a, doc_b):
        s1 = self.__fn(doc_a)
        s2 = self.__fn(doc_b)

        changes = set({})
        flag = "44b779b6324c285dd"

        # Computing delta
        diff = difflib.unified_diff(s1, s2, fromfile=flag, tofile=flag)
        for line in diff:
            if self.is_diff_valid(line, flag):
                changes.add(line)
        return changes
    
    def is_diff_valid(self, line, flag):
        return (
            (line.startswith("+") or line.startswith("-")) and
            (flag not in line) and
            ("<!--" not in line) and
            (not line.endswith("-->"))
        )

class Runner:
    """ Entity that knows how to explore a configuration based on a given verifier. """

    def __init__(self, verifier):
        self._verifier = verifier

    def run(self, config):
        return set({})


class Configuration:
    """ Represents a CMS-agnostic configuration. """

    def __init__(self, plugins):
        self.__config_sequence = [p for p in plugins]
        self.__config = frozenset(self.__config_sequence)

    def difference(self, other):
        return Configuration(self.__config.difference(other.__config))

    @staticmethod
    def factory(plugins):
        return Configuration(plugins)

    def __getitem__(self, item):
        return self.__config_sequence[item]

    def __setitem__(self, key, value):
        self.__config_sequence[key] = value

    def __len__(self):
        return len(self.__config)

    def __contains__(self, item):
        if isinstance(item, self.__class__):
            return item.__config.issubset(self.__config)
        return False

    def __str__(self):
        return "[" + ", ".join(self.__config_sequence) + "]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__config == other.__config
        return False

    def __hash__(self):
        return hash(self.__config)


class CMSInterface:
    """ Represents a CMS command line interface. """

    def plugins(self):
        return ()

    def activate(self, plugins):
        pass

    def deactivate(self, plugins):
        pass


class WebDriver:
    def __init__(self, url):
        self.__address = url
        self.__html_dir = tempfile.mkdtemp()
        logging.debug(self.__html_dir)

    def fetch(self):
        response = None
        for _ in range(5):
            try:
                response = urllib.request.urlopen(self.__address)
                break
            except:
                pass
        
        if not response:
            raise Exception('Cannot fetching page {}. Please, check WordPress console log'.format(self.__address))
        
        html_raw = response.read()
        parser = BeautifulSoup(html_raw, 'html.parser')
        html_content = parser.prettify().encode('UTF-8')
        return html_content

    def html_document_path(self, name):
        return os.path.join(self.__html_dir, "{}.html".format(name))

    def save(self, html, name):
        document_path = self.html_document_path(name)
        with open(document_path, "wb") as html_file:
            html_file.write(html)

    def cleanup(self):
        shutil.rmtree(self.__html_dir)


def fetch_plugins_page(plugins, web_driver, cli):
    plugins_pages = {}
    logging.info("STEP - fetching pages started")
    
    cli.deactivate(plugins)
    plugins_off_html = web_driver.fetch()
    web_driver.save(plugins_off_html, "none")
   
    for plugin in plugins:
        logging.info("Processing plugin {}".format(plugin))
        cli.activate([plugin])
        html, plugin_on_html, is_valid = None, None, False
        for _ in range(5):
            try:
                html = web_driver.fetch()
                plugin_on_html = web_driver.fetch()
                is_valid = True
            except:
                # some plugins take a while to fetch the page
                # to fix that need to try fetch more than once
                continue
	    
        if not is_valid:
            raise Exception('Cannot fetch page for {}'.format(plugin))
        
        web_driver.save(plugin_on_html, plugin)
        plugins_pages[plugin] = html
        cli.deactivate([plugin])
    
    logging.info("STEP - fetching pages finished")
    return plugins_pages


def dimensionality_reduction(plugins, web_driver, cli, skip=False):
    plugins_pages = fetch_plugins_page(plugins, web_driver, cli)
    
    if skip:
        return plugins

    logging.info("STEP - dimensionality reduction started")
    clusters = OrderedDict()

    for plugin, html in plugins_pages.items():
        hash_value = hashlib.md5(html).hexdigest()
        if hash_value in clusters.keys():
            clusters[hash_value].append(plugin)
        else:
            clusters[hash_value] = [plugin]

    logging.info("Reducing configuration")
    reduced_plugins = []
    for cluster in clusters.values():
        reduced_plugins.append(cluster[len(cluster) >> 1])
    logging.debug("Input: {}, Reduced:{}".format(len(plugins), len(reduced_plugins)))

    logging.info("STEP - dimensionality reduction finished")
    return reduced_plugins


def plain_html(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines() if is_valid(line)]


def html_text(file_path):
    with open(file_path) as f:
        parser = BeautifulSoup(f, "html.parser")
        return [line.strip() for line in parser.get_text().splitlines() if is_valid(line)]


def is_valid(line):
    return (not line == "\ufeff") and len(line.strip())


def check_frequency(conflicts):
    freq = {}
    for config in conflicts:
        for plugin in config:
            if plugin in freq.keys():
                freq[plugin] += 1
            else:
                freq[plugin] = 1
    return freq
