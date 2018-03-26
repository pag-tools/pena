import os, time, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

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
        # self.timerScreen = QTimer()
        # self.timerScreen.setInterval(5000)
        # self.timerScreen.setSingleShot(True)
        # self.timerScreen.timeout.connect(self.refresh_page)
        # self.loadFinished.connect(self.timerScreen.start)

        # self.loadFinished.connect(self.timerScreen.start)
        # self.refresh_page()

    def refresh_page(self):
        # timer to wait for load finished
        self.load(QUrl(self.url))  

    def create_dir(self, _dir):
        if _dir not in os.listdir():
            try:
                os.mkdir(_dir)
            except FileExistsError as e:
                pass

    def capture(self, output_file):
        # loads a url and wait
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
        print('loading...')
        time.sleep(1)

    def _loadFinished(self, result):
        self._loaded = True
