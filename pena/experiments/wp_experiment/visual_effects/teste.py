from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class browser(QWebView):
    def __init__(self, parent=None):
        super(browser, self).__init__(parent)
        self.size = QSize(1920, 1460)

        self.timerScreen = QTimer()
        self.timerScreen.setInterval(2000)
        self.timerScreen.setSingleShot(True)
        self.timerScreen.timeout.connect(self.takeScreenshot)

        self.loadFinished.connect(self.timerScreen.start)

    def load_url(self):
        self.load(QUrl("http://localhost:8081"))

    def takeScreenshot(self):
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(self.size)
        
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        
        painter = QPainter(image)
        frame.render(painter)
        painter.end()

        image.save('both' + ".png")

        sys.exit()

if __name__ == "__main__":
    import  sys        
    app  = QApplication(sys.argv)
    main = browser()
    main.load_url()
    app.exec_()