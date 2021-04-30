# this is the MAIN file
# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import sys

from constants import *
from midiInput import MidiInput
from staff import Staff
from key import Key
from labeling import Labeling

class Window(QMainWindow):

    def __init__(self):
        super().__init__()      # exended from class QMainWindow
        self.title = "Improvisation App"
        self.top = WINDOW_UPPER_LEFT_X
        self.left = WINDOW_UPPER_LEFT_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        # init buttons, keyboard and window
        self.staff = Staff()
        self.init_buttons()
        self.init_keyboard(88)
        self.init_window()
        # instance of staff
        self.labeling = Labeling()
        self.labeling.init_label(self)
        # timer to update the application
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(10)
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start()


    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def init_keyboard(self, num_keys):
        self.keys = []
        for i in range(num_keys):
            self.keys.append(Key(i, self.staff))

    def init_buttons(self):
        # play
        play_button = QPushButton('Play', self)
        play_button.setToolTip('to start playing the Backing Track')
        play_button.move(100,70)
        play_button.clicked.connect(self.on_click_play)
        # pause
        pause_button = QPushButton('Pause', self)
        pause_button.setToolTip('to pause the Backing Track')
        pause_button.move(200,70)
        pause_button.clicked.connect(self.on_click_pause)
        # stop
        stop_button = QPushButton('Stop', self)
        stop_button.setToolTip('to stop the Backing Track')
        stop_button.move(300,70)
        stop_button.clicked.connect(self.on_click_stop)
        # record
        record_button = QPushButton('Record', self)
        record_button.setToolTip('to record your playing')
        record_button.move(907,280)
        record_button.clicked.connect(self.on_click_record)
        # listen
        listen_button = QPushButton('Play recording', self)
        listen_button.setToolTip('to listen to your recording')
        listen_button.resize(120,26)
        listen_button.move(1007,280)
        listen_button.clicked.connect(self.on_click_listen)
        #listen_button.setDisabled(True)

    @pyqtSlot()
    def on_click_play(self):
        self.staff.play_bt()

    @pyqtSlot()
    def on_click_pause(self):
        self.staff.pause_bt()

    @pyqtSlot()
    def on_click_stop(self):
        self.staff.stop_bt()

    @pyqtSlot()
    def on_click_record(self):
        midi_input.record_input()

    @pyqtSlot()
    def on_click_listen(self):
        print('on click listen')
        midi_input.listen_to_recording()
        #midi_input.record_input()

    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
        painter = QPainter(self)    # create the object of QPainter class
        # draw Notelines from staff.py
        self.staff.draw(painter)
        # draw keyboard and marker from key.py
        for key in WHITE_KEYS:
            key.draw(painter)
        for key in BLACK_KEYS:
            key.draw(painter)
        midi_input.draw(painter)
        return

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
window = Window()
midi_input = MidiInput()

sys.exit(App.exec())