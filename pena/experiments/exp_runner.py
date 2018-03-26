#!/usr/bin/env python3
import os
from .wpcapacity.wpcapacity import WPCapacity
from .efficiency.efficiency import Efficiency
from experiments.black_list import BLACK_LIST
from experiments.setup import all_plugins

wordpress_path = '../environment/wordpress/wordpress'

input_plugins = all_plugins()
##########
wpcapacity = WPCapacity(wp_path=wordpress_path)
wpcapacity.run(input_plugins)
##########
efficiency = Efficiency(wp_path=wordpress_path)
single = efficiency.run(input_plugins)
multiple = efficiency.run(input_plugins)
