'''
Names: J. Boon, F. Hoetjes, J. Siegers, V. Vlugt & L. van der Waals
MM_Group: 3
Study: BSc Informatica
main.py:
    - Acts as the main, in which the application itself can be executed.
    - Contains the GUI and all of its features
    - Manages the webcam and all the images which are used in the GUI.
'''

import image_processing.image_processing as ip
from app import Application
import time
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
import cv2
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import matplotlib
import subprocess
import os
matplotlib.use("Qt5Agg")

FPS = 10
FILEPATH = os.path.abspath(__file__)

difficulty = "Medium"
first = "Player"
start = False


class MainThread(QThread):
    '''
    Main thread which manages webcam and images in GUI.
    '''

    changePixmap = pyqtSignal(QImage)
    changeDebugPixmap = pyqtSignal(QImage)
    changeContourPixmap = pyqtSignal(QImage)

    def __init__(self, qt_instance, app):
        super().__init__(qt_instance)
        self.app = app
        self.threadActive = True

    def run(self):
        '''
        Main run function, sets up main loop and captures image from webcam
        every loop. Gets output images from app and displays it in GUI.
        '''

        # Setup video capture source
        cap = cv2.VideoCapture(0)

        while self.threadActive:
            time.sleep(1/FPS)

            ret, frame = cap.read()
            frame = frame[:, 90:550]
            frame = np.flip(frame, (0, 1))
            frame = frame.copy()

            self.set_image_in_gui(ret, frame)
            self.set_debug_image_in_gui(ret, frame)

            affined_image = self.app.update(frame)
            # if affined_image is None:
            #     affined_image = frame
            if affined_image is None:
                affined_image = frame
            self.set_contour_image_in_gui(ret, affined_image)

            if self.app.game_finished:
                self.threadActive = False

            # self.set_contour_image_in_gui(ret, contour_image)

        # Open new proces and quit current app.
        subprocess.Popen([sys.executable, FILEPATH])
        app.quit()

    def set_image_in_gui(self, ret, frame):
        '''
        Sets the main image in the GUI (the camera).
        '''
        if ret:
            h, w, ch = frame.shape
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = ch * w

            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def set_debug_image_in_gui(self, ret, frame):
        '''
        Sets the preprocessed debug image in the GUI.
        '''

        im = ip.preprocess_image(frame)

        if ret:
            h, w = im.shape
            bytesPerLine = w

            convertToQtFormat = QImage(
                im.data, w, h, bytesPerLine, QImage.Format_Grayscale8)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changeDebugPixmap.emit(p)

    def set_contour_image_in_gui(self, ret, frame):
        '''
        Sets the transformed output image in the GUI.
        '''

        if ret:
            h, w, ch = frame.shape
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = w * ch

            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio)
            self.changeContourPixmap.emit(p)


class GUI(QMainWindow):
    '''
    This class manages loading the PyQTwindows and binds to components from
    PyQT
    '''

    def __init__(self, *args):
        QMainWindow.__init__(self)
        loadUi("gui/TicTacToe.ui", self)
        self.setWindowTitle("TicTacToeTwo")
        self.pushButton.clicked.connect(self.button)

    def setImage(self, image):
        self.image_display.setPixmap(QPixmap.fromImage(image))

    def setDebugImage(self, image):
        self.debug_image_display.setPixmap(QPixmap.fromImage(image))

    def setContourImage(self, image):
        self.contour_image_display.setPixmap(QPixmap.fromImage(image))

    def hide(self):
        '''
        Hide options from GUI when game has started.
        '''
        self.comboBox.hide()
        self.comboBox_2.hide()
        self.label.hide()
        self.label_2.hide()
        self.label_5.hide()
        self.label_6.hide()

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

        if start is False:
            # Read values from boxes and start application.
            difficulty = self.comboBox.currentText()
            first = self.comboBox_2.currentText()
            self.pushButton.setText("Restart")
            self.hide()
            start = True

            app = Application(difficulty, first)
            self.th = MainThread(self, app)

            self.th.changePixmap.connect(self.setImage)
            self.th.changeDebugPixmap.connect(self.setDebugImage)
            self.th.changeContourPixmap.connect(self.setContourImage)

            self.th.start()
        else:
            # Break out of update loop.
            self.th.threadActive = False


if __name__ == "__main__":
    app = QApplication([])
    form = GUI()
    form.show()
    sys.exit(app.exec_())
