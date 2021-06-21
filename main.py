import image_processing.image_processing as ip
from app import Application
import time
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
import cv2
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import matplotlib
matplotlib.use("Qt5Agg")

FPS = 10


class MainThread(QThread):
    changePixmap = pyqtSignal(QImage)
    changeDebugPixmap = pyqtSignal(QImage)
    changeContourPixmap = pyqtSignal(QImage)

    def __init__(self, qt_instance, app):
        super().__init__(qt_instance)
        self.app = app

    def run(self):
        # Setup video capture source
        cap = cv2.VideoCapture(0)

        while True:
            time.sleep(1/FPS)

            ret, frame = cap.read()
            frame = frame[100:380, 180:460]

            self.set_image_in_gui(ret, frame)
            self.set_debug_image_in_gui(ret, frame)

            contour_image = self.app.update(frame)

            self.set_contour_image_in_gui(ret, contour_image)

    def set_image_in_gui(self, ret, frame):
        if ret:
            h, w, ch = frame.shape
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = ch * w

            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def set_debug_image_in_gui(self, ret, frame):
        im = ip.preprocess_image(frame)

        if ret:
            h, w = im.shape
            bytesPerLine = w

            convertToQtFormat = QImage(
                im.data, w, h, bytesPerLine, QImage.Format_Grayscale8)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changeDebugPixmap.emit(p)

    def set_contour_image_in_gui(self, ret, frame):
        if ret:
            h, w, ch = frame.shape
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = w * ch

            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changeContourPixmap.emit(p)




class GUI(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        window = loadUi("gui/TicTacToe.ui", self)
        self.setWindowTitle("TicTacToe")

        app = Application()
        th = MainThread(self, app)

        th.changePixmap.connect(self.setImage)
        th.changeDebugPixmap.connect(self.setDebugImage)
        th.changeContourPixmap.connect(self.setContourImage)
        th.start()

    def setImage(self, image):
        self.image_display.setPixmap(QPixmap.fromImage(image))

    def setDebugImage(self, image):
        self.debug_image_display.setPixmap(QPixmap.fromImage(image))

    def setContourImage(self, image):
        self.contour_image_display.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication([])
    form = GUI()
    form.show()
    sys.exit(app.exec_())
