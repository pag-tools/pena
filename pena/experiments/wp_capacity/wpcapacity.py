#!/usr/bin/env python3
from subprocess import check_output
from time import time
import csv, ast, os

BLACK_LIST = [
    "woocommerce-improved-external-products",  # Total crash
    "we-will-call-you",  # Attempts to fetch external resource but fails to open stream
    "social-media-aggregator",  # Error when activated with wp-scroll-up
    "revcanonical",  # Uncaught Error: Call to undefined function spliti()
    "hooknews",  # Uncaught Error: Call to undefined function mysql_query()
    "cystats",  # Uncaught Error: Call to undefined function mysql_query()
    "easy-calendar",  # Uncaught Error: Call to undefined function spliti()
    "facebook",  # PHP Fatal error: 'break' not in the 'loop' or 'switch' context
    "less",  # PHP Fatal error:  Uncaught Error: Call to undefined function eregi_replace()
    "paypal-for-woocommerce",
    "quiz-master-next",
    "wp-force-ssl",
    "wp-force-https",
    "mailchimp-for-woocommerce",
    "eps-301-redirects",
    "ip-loc8",
    "our-team-enhanced",
    "easy-pie-coming-soon", # PHP Fatal error: Uncaught Error: Call to a member function set_background_type()
    "bad-behavior",
    "paid-memberships-pro",
    "accesspress-social-share",
    "head-cleaner"
]



class WPCapacity:
    def __init__(self, wp_path):
        self.wp_path = wp_path
        self.csv_filename = "wp-capacity-all.csv"
        self.plugins_csv = "plugins.csv"

    def get_plugins(self):
        """
        Description:
            Get plugins name from plugins.csv
        Params:
            None
        Return:
            list of plugins name
        """
        with open(self.plugins_csv) as f:
            return ast.literal_eval(f.read())

    def run(self, plugins, mode="default"):
        """
        Description:
            Runner to get activation time
        Params:
            plugins: list of plugins (list)
        Optional Params:
            mode: choose 'default' if run with default WP settings
                  choose 'modified' if run with WP settings modified (manual step)
        Return:
            data: Dict with activation time for each plugin (Dictionary)
        """
        data = {}
        counter = 1

        for plugin in plugins:
            if plugin in BLACK_LIST:
                continue
            
            activate_time = self.calculate_activation(plugin)            
           
            _data = {
                "n": counter,
                "name": plugin,
                "acttime": activate_time,
                "mode": mode
            }
            
            data[counter] = _data
            counter += 1

            self.deactive_plugin(plugin)

        self.generate_csv(self.csv_filename, dict_execution)

    def deactive_plugin(self, plugin):
        """
        Description:
            Deactivate plugin on WP
        Params:
            plugin: plugin name (string)
        Return:
            None
        """
        path = "--path={}".format(self.wp_path)
        try:
            check_output(["wp", "plugin", "deactivate", plugin, path])
        except:
            pass

    def generate_csv(self, filename, data):
        """
        Description:
            Generate the file with execution data
        Params:
            filename: CSV filename (String)
            data: Dictionary with data generate by run method
        Return:
            None
        """
        with open(filename, "w") as csv_file:
            headers = ["n", "plugin", "get_time", "activation_time", "mode"]
            file = csv.DictWriter(csv_file, fieldnames=headers)
            file.writeheader()
            for line in dict_execution.values():
                data = {
                    "n": line["n"],
                    "plugin": line["name"],
                    "activation_time": line["acttime"],
                    "mode": line["mode"]
                }
                file.writerow(data)

    def calculate_activation(self, plugin_name):
        """
        Description:
            Calculate activation time of a plugin
        Params:
            plugin_name: string
        Return:
            time spent to activate a plugin (float)
        """
        path = "--path={}".format(self.wp_path)
        print("try to activate: {}".format(plugin_name))
        try:
            init = time()
            check_output(["wp", "plugin", "activate", plugin_name, path])
        except Exception as e:
            print(e)
            self.deactive_plugin(plugin_name)
        
        return (time() - init)

WP_URL = "../../environment/wordpress/wordpress"
wpcapacity = WPCapacity(WP_URL)

plugins = wpcapacity.get_plugins()[0:400]
wpcapacity.run(plugins)