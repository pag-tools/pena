import sys, time, os, ast, csv
from subprocess import check_output
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from similarity import Similarity

class Screenshot(QWebView):
    def __init__(self, _dir):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)
        self.url = 'http://localhost:8081/'
        self._dir = _dir
        self.create_dir(_dir)
        self.size = QSize(1920, 1460)

    def create_dir(self, _dir):
        if _dir not in os.listdir():
            try:
                os.mkdir(_dir)
            except FileExistsError as e:
                pass

    def capture(self, output_file):
        self.load(QUrl(self.url))
        self.wait_load()
        
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(self.size)
        
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
       
        image.save('{}'.format(output_file))

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True


class WordPressCMS:
    def __init__(self, wp_path):
        self.wp_path = wp_path

    def activate(self, plugin_name, is_list=False):
        if not is_list:
            try:
                check_output(['wp','plugin','activate', plugin_name, '--path={}'.format(self.wp_path)])
            except:
                self.deactivate(plugin_name)

    def deactivate(self, plugin_name, is_list=False):
        if not is_list:
            try:
                check_output(['wp','plugin','deactivate', plugin_name, '--path={}'.format(self.wp_path)])
            except Exception as e:
                raise Exception('Cannot deactivate plugin: {}'.format(plugin_name))
        else:
            for plugin in plugin_name:
                try:
                    check_output(['wp','plugin','deactivate', plugin, '--path={}'.format(self.wp_path)])
                except Exception as e:
                    raise Exception('Cannot deactivate plugin: {}'.format(plugin))

def list_to_string(obj):
    return str(obj).replace('[','').replace(']','').replace("'",'').strip()

wp = WordPressCMS(wp_path='../../../environment/wordpress/wordpress/')
screenshot = Screenshot(_dir='screenshots')

with open('CONFLICTS-PRECISION-ALL') as f:
    CONFLICTS = ast.literal_eval(f.read())
    for conflict in CONFLICTS:
        print('deactivating: {}'.format(conflict))
        wp.deactivate(conflict, is_list=True)

# capture screenshot from test page without plugins activated
default_page = '{}/default_page.png'.format(screenshot._dir)
screenshot.capture(default_page)

tinit = time.time()
with open('visual_conflicts.csv', 'w') as visual:
    visual_csv = csv.DictWriter(visual, fieldnames=['conflict', 'visual_effects'])
    visual_csv.writeheader()
    for conflict in CONFLICTS:
        print('running {}'.format(conflict))

        p1, p2 = conflict[0], conflict[1]
        conflict = list_to_string(conflict)
        
        # creating a folder for each conflict
        conflict_dir = ''.join([screenshot._dir, '/', conflict])
        screenshot.create_dir(conflict_dir)
                    
        # taking screenshot from first plugin
        wp.activate(p1)
        p1_path = '{}/{}.png'.format(conflict_dir, p1)
        screenshot.capture(p1_path)
        
        # check similarity between
        wp.deactivate(p1)

        # taking screenshot from second plugin
        wp.activate(p2)
        p2_path = '{}/{}.png'.format(conflict_dir, p2)
        screenshot.capture(p2_path)

        # taking screenshot from both plugins (p2 already activated)
        wp.activate(p1)
        both_path = '{}/both.png'.format(conflict_dir)
        screenshot.capture(both_path)

        # deactivating both plugins
        wp.deactivate(p1)
        wp.deactivate(p2)
        
        # check similarity between images
        image_checker = Similarity(default_page, p1_path, p2_path, both_path, conflict_dir)
        is_changed = image_checker.is_changed_page()
      
        visual_csv.writerow({'conflict': conflict, 'visual_effects': is_changed})