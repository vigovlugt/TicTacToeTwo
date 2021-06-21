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
import subprocess, os
matplotlib.use("Qt5Agg")

FPS = 10
FILEPATH = os.path.abspath(__file__)

difficulty = "Medium"
first = "Player"
start = False

class MainThread(QThread):
    changePixmap = pyqtSignal(QImage)
    changeDebugPixmap = pyqtSignal(QImage)
    changeContourPixmap = pyqtSignal(QImage)

    def __init__(self, qt_instance, app):
        super().__init__(qt_instance)
        self.app = app
        self.threadActive = True

    def run(self):
        # Setup video capture source
        cap = cv2.VideoCapture(0)

        while self.threadActive:
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

    def stop(self):
        '''
        Stop thread for safe exit of program.
        '''
        self.threadActive = False
        self.sleep(1) # Allow for thread to safely exit.

class GUI(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        window = loadUi("gui/TicTacToe.ui", self)
        self.setWindowTitle("TicTacToeTwo")
        self.pushButton.clicked.connect(self.button)

    def setImage(self, image):
        self.image_display.setPixmap(QPixmap.fromImage(image))

    def setDebugImage(self, image):
        self.debug_image_display.setPixmap(QPixmap.fromImage(image))

    def setContourImage(self, image):
        self.contour_image_display.setPixmap(QPixmap.fromImage(image))

    def button(self):
        '''
        Executes when 'Start'/'Restart' button is clicked in UI. If button is
        'Start', start var is False and application will be created. If button
        is 'Restart', then start var is True and new subprocess will be created
        while the current process will quit.
        '''
        global start
        global difficulty
        global first

        if start == False:
            # Read values from boxes and start application.
            difficulty = self.comboBox.currentText()
            first = self.comboBox_2.currentText()
            self.pushButton.setText("Restart")
            start = True

            app = Application(difficulty, first)
            self.th = MainThread(self, app)

            self.th.changePixmap.connect(self.setImage)
            self.th.changeDebugPixmap.connect(self.setDebugImage)
            self.th.start()
        else:
            # Open new subprocess, stop thread and exit.
            subprocess.Popen([sys.executable, FILEPATH])
            self.th.stop()
            sys.exit(0)

if __name__ == "__main__":
    app = QApplication([])
    form = GUI()
    form.show()
    sys.exit(app.exec_())
