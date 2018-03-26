import logging, hashlib, time, copy
from tname.core.execution import SplitSearch
from tname.core.cms import WordPressCLI
from tname.core.model import WebDriver, Verifier, Configuration, plain_html, check_frequency
from tname.core.model import dimensionality_reduction
from tname.core.visual_oracle.visual_oracle import VisualOracle
from tname.core.visual_oracle.screenshot import Screenshot
from tname.core.analyser import Analyser
from tname.core.timer import Timer

class PENA:
    def __init__(self, cms_path, url="http://localhost", heuristic=plain_html, debug=True):
        """
        Params:
            cms_path: path for wordpress folder
            url: wordpress index page url (default is http://localhost)
            heuristic: type of heuristic used to check page conflict
            debug: test pages will not been removed after execution (check ~/tmp/ folder)
        """
        self.cli = WordPressCLI(home=cms_path)
        self.web_driver = WebDriver(url=url)
        self.heuristic = heuristic
        self.debug = debug
        self.verifier = Verifier(self.cli, self.web_driver, self.heuristic)
        self.input_plugins = []
        self.mode = SplitSearch
        self.generate_configuration = False
        self.show_lines = True
        self.skip_dimensionality = False
        self.remove_spurious = True
        self.visual_oracle = True

    def set_input_plugins(self, input_plugins):
        """
            Description:
                Sets a list of plugins into a configuration
            Params:
                input_plugins: list of plugins name
            Return:
                None
        """
        self.input_plugins = input_plugins

    def set_mode(self, mode):
        """
            Description:
                Set a Search technnique to check conflicts
            Params:
                mode: SplitSearch | Pairwise (class)
            Return:
                None
        """
        self.mode = mode

    def set_generate_configuration(self, generate):
        """
            Description:
                Set true to generate a dictionary of conflicts
            Params:
                generate: boolean
            Return:
                None
        """
        self.generate_configuration = generate

    def set_show_lines(self, show_lines):
        """
            Description:
                Shows unexpected code added/removed from a plugin in log    
            Params:
                show_lines: boolean
            Return:
                None
        """
        self.show_lines = show_lines

    def set_skip_dimensionality(self, skip):
        """
            Description:
                Set true to run input_plugins without dimensionality reduction
            Params:
                skip: boolean
            Return:
                None
        """
        self.skip_dimensionality = skip
    
    def run_only_dimensionality(self, input_plugins=[]):
        """
        Description:
            Runs only dimensionality reduction to generate a set of plugins with differents equivalence class
        Params:
            input_plugins: list of plugins name
        Return:
            list of plugins after dimensionality reduction
        """
        reduced_plugins = dimensionality_reduction(input_plugins, self.web_driver, self.cli)
        if len(reduced_plugins):
            logging.debug("Plugins after dimensionality reduction")
            [logging.debug(" {}".format(plugin)) for plugin in reduced_plugins]
        return reduced_plugins

    def run(self):
        """
        Description:
            PENA Runner
        Params:
            None
        Return:
            None
        """
        if len(self.input_plugins) < 2:
            raise Exception('Plugin list invalid. The plugin list must have lenght 2 or more.')

        # deactivate plugins
        self.cli.deactivate(self.input_plugins)
        
        logging.info('RUNNING {}'.format(str(self.mode)))
        logging.info('RUNNING N={}'.format(len(self.input_plugins)))
        
        logging.info("Run Started")

        technnique = self.mode(self.verifier)

        # STEP 1 - DIMENSIONALITY REDUCTION
        reduced_plugins = dimensionality_reduction(
            self.input_plugins,
            self.web_driver, 
            self.cli, 
            skip=self.skip_dimensionality
        )
        
        # STEP 2 and 3 - SEARCH FOR CONFLICTS AND CLUSTERING
        if len(reduced_plugins) > 1:
            configuration = Configuration(reduced_plugins)
            conflicts = technnique.run(configuration)
            logging.info("Delta timer (in minutes): {}".format(Timer.get_delta()))
          
            if self.generate_configuration:
                ''' generate nodes of conflicts '''
                self.generate_nodes(reduced_plugins, conflicts)
                return

            if conflicts:
                all_conflicts = copy.copy(conflicts)

                # REPORT CONFLICTS FOUND BEFORE CLEANSING
                logging.debug("Conflicts found after searching: {}".format(len(all_conflicts)))
                for conflict in all_conflicts:
                    logging.debug("Conflict - {}".format(conflict))
                    changes = self.verifier.conflicting_changes(conflict)
                    unexpected_added, unexpected_removed = changes[0], changes[1]
                    if len(unexpected_added):
                        added = [("    {}".format(line)) for line in unexpected_added]
                        logging.info("{}: {}".format("Unexpected added", added))
                    if len(unexpected_removed):
                        removed = [("    {}".format(line)) for line in unexpected_removed]
                        logging.info("{}: {}".format("Unexpected removed", removed))

                # STEP 4 - REPORT CLEANSING
                if self.remove_spurious:
                    logging.info("Cleansing started")
                    
                    self.cleansing_data = {
                        "non-determinism": [],
                        "minify": [],
                        "union_tags": [],
                        "optional_closing": []
                    }
                    
                    temp_conflicts = copy.copy(all_conflicts)
                    for conflict in all_conflicts:
                        changes = self.verifier.conflicting_changes(conflict)
                        unexpected_added, unexpected_removed, typeof_removal = Analyser(changes[0], changes[1]).run()
                        if (not unexpected_added) and (not unexpected_removed):
                            self.cleansing_data[typeof_removal].append(conflict)
                            temp_conflicts.remove(conflict)
                        else:
                            self.verifier.update_changes(conflict, unexpected_added, unexpected_removed)
                    
                    remaining_conflicts = self.cleansing(temp_conflicts)
                    
                    self.report_cleansing_data(len(temp_conflicts) - len(remaining_conflicts))
                    logging.info("Cleansing finished")
                    all_conflicts = remaining_conflicts

                # STEP 5 - VISUAL ORACLE
                if self.visual_oracle:
                    logging.info("Checking visual conflicts started")
                    visual_conflicts = self.get_visual_conflicts(all_conflicts)
                    for conflict in visual_conflicts:
                        logging.info('Visual conflict identified: {}'.format(conflict))
                    logging.info("Checking visual conflicts finished")
                    
                # REPORT CONFLICTS
                logging.debug("===== FINAL REPORT =====")
                for conflict in all_conflicts:
                    logging.debug(conflict)
                    logging.debug("Conflicting config - {}".format(conflict))
                    
                    if self.show_lines:
                        changes = self.verifier.conflicting_changes(conflict)
                        unexpected_added, unexpected_removed = changes[0], changes[1]
                        if len(unexpected_added):
                            added = [("    {}".format(line)) for line in unexpected_added]
                            logging.info("{}: {}".format("Unexpected added", added))
                        if len(unexpected_removed):
                            removed = [("    {}".format(line)) for line in unexpected_removed]
                            logging.info("{}: {}".format("Unexpected removed", removed))
                    
                freq = check_frequency(all_conflicts)
                [logging.debug("{}: {}".format(k, v)) for k, v in freq.items()]

                self.cli.deactivate(self.input_plugins)
        
        logging.info("Run Finished!")

        if not self.debug:
            self.web_driver.cleanup()

    def generate_nodes(self, plugins, conflicts):
        """
        Description:
            Generate a data structure (Dictionary) with all conflicts found by PENA
        Params:
            plugins: list of plugins name
            conflicts: all conflicts found by Pena
        """
        _file = 'configuration-{}-{}.txt'.format(len(plugins), time.asctime())
        configuration = {}
        for i in plugins:
            # start all keys with empty list
            configuration[i] = []

        while len(conflicts) != 0:
            conflict_list = conflicts.pop()
            first, second = conflict_list[0], conflict_list[1]

            if second not in configuration[first]:
                configuration[first].append(second)
            if first not in configuration[second]:
                configuration[second].append(first)

        with open(_file, 'w') as f:
            f.write(str(configuration))

    def rerun(self, conflicts):
        """ 
        Description:
            Remove conflicts non-deterministics found by PENA
        Params:
            conflicts: list of conflicts       
        Return:
            List of conflicts without non-deterministics conflicts
        """
        if not conflicts:
            return conflicts
        
        self.cli.deactivate(self.input_plugins)

        non_deterministic_conflicts = []
        for conflict in conflicts:
            try:
                self.cli.activate(conflict)
                plugins_on_html = self.web_driver.fetch()
                hash_value = hashlib.md5(plugins_on_html).hexdigest()
                self.cli.deactivate(conflict)
                
                self.cli.activate(conflict)
                plugins_on_html = self.web_driver.fetch()
                self.cli.deactivate(conflict)
            except Exception as e:
                self.cli.deactivate(conflict)

            if hash_value != hashlib.md5(plugins_on_html).hexdigest():
                self.cleansing_data["non-determinism"].append(conflict)
                non_deterministic_conflicts.append(conflict)
                
        [conflicts.remove(conflict) for conflict in non_deterministic_conflicts]
        return conflicts
   
    def cleansing(self, conflicts):
        """
        Description:
            Remove spurious from final report
        Params:
            conflicts: array of conflicts
        Optional Params:
            None
        Return:
            Conflicts list after remove spurious
        """
        cleansing_conflicts = [conflict for conflict in conflicts]

        # remove conflicts with minify keyword
        for conflict in conflicts:
            if 'minify' in str(conflict):
                self.cleansing_data["minify"].append(conflict)
                cleansing_conflicts.remove(conflict)
        
        # rerun to check non-determinism conflicts
        
        cleansing_conflicts = self.rerun(cleansing_conflicts)

        return cleansing_conflicts

    def get_visual_conflicts(self, conflicts):
        """
        Description:
            Check visual discrepance between plugins
        Params:
            conflicts: array of plugins
        Optional Params:
            None
        Return:
            array of conflicts that shows visual conflicts
        """
        screenshot = Screenshot()
        visual_oracle = VisualOracle(conflicts, self.cli, screenshot)
        visual_conflicts = visual_oracle.run()
        return visual_conflicts

    def report_cleansing_data(self, total_conflicts):
        logging.info("Conflicts removed by cleansing: {}".format(total_conflicts))
        logging.info("non-determinism conflicts: {}".format(len(self.cleansing_data["non-determinism"])))
        logging.info("{}".format(self.cleansing_data["non-determinism"]))
        logging.info("minify conflicts: {}".format(len(self.cleansing_data["minify"])))
        logging.info("{}".format(self.cleansing_data["minify"]))
        logging.info("union conflicts: {}".format(len(self.cleansing_data["union_tags"])))
        logging.info("{}".format(self.cleansing_data["union_tags"]))
        logging.info("optional closing conflicts: {}".format(len(self.cleansing_data["optional_closing"])))
        logging.info("{}".format(self.cleansing_data["optional_closing"]))