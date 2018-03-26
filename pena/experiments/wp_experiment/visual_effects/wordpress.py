from subprocess import check_output

class WordPressCMS:
    def __init__(self, wp_path):
        self.wp_path = wp_path

    def is_list(self, obj):
        return type(obj) == type([])

    def activate(self, plugins=[]):
        if not self.is_list(plugins):
            raise Exception('Cannot activate {}, use a list instead [p1, p2, ...]'.format(plugins))

        for plugin in plugins:
            try:
                check_output(['wp','plugin','activate', plugin, '--quiet', '--path={}'.format(self.wp_path)])
            except:
                self.deactivate(plugins)
                raise Exception('Cannot activate plugin: {}'.format(plugin))

    def deactivate(self, plugins=[]):
        if not self.is_list(plugins):
            raise Exception('Cannot deactivate {}, use a list instead [p1, p2, ...]'.format(plugins))
        
        for plugin in plugins:
            try:
                print('deactivating: {}'.format(plugin))
                check_output(['wp','plugin','deactivate', plugin, '--quiet','--path={}'.format(self.wp_path)])
            except:
                raise Exception('Cannot deactivate plugin: {}'.format(plugin))