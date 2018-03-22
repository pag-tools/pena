from PyQt4.QtCore import QUrl, QSize
from PyQt4.QtGui import QApplication, QImage, QPainter
from PyQt4.QtWebKit import QWebView, QWebSettings
import sys, time, os, locale

class Screenshot(QWebView):
    def __init__(self, imgs_dir=None):
        self.app = QApplication(sys.argv)
        locale.setlocale(locale.LC_ALL, "C")
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)
        self.url = "http://localhost:8081/"
        self.imgs_dir = imgs_dir if imgs_dir else time.asctime()
        self.create_dir(self.imgs_dir)
        self.size = QSize(1920, 1460)
        self.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
    
    def create_dir(self, directory):
        """ create a folder to store the images taken """
        try:
            os.mkdir("{}".format(directory))
        except FileExistsError as e:
            # folder already exists
            pass
        except Exception as e:
            raise Exception(e)

    def capture(self, output_file):
        """ capture a screenshot from WebView """
        if ".png" not in output_file:
            raise Exception("Err: image format invalid, please save with png extension.")

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
        image.save("{}".format(output_file))

    def wait_load(self, delay=1):
        """ wait processes to load the page """
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True