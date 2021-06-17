import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from motion_detection.motion_detection import MotionDetection
import time


class Webcam(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            time.sleep(1/10)
            ret, frame = cap.read()
            y = self.md.process_image(frame)
            print(y)
            if ret:
                h, w, ch = frame.shape
                # end = w - (w - h) // 2
                # start = (w - h) // 2
                # print(start, end)
                # frame = frame[:, start: end]
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = ch * w

                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class TicTacToe(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        window = loadUi("gui/TicTacToe.ui", self)
        self.setWindowTitle("TicTacToe")
        # self.image_display = QLabel(self)
        # self.image_display.resize(1000, 1000)
        # self.image_display.move(0, 0)
        th = Webcam(self)
        th.md = MotionDetection()
        th.changePixmap.connect(self.setImage)
        th.start()

    def setImage(self, image):
        self.image_display.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication([])
    form = TicTacToe()
    form.show()
    sys.exit(app.exec_())
