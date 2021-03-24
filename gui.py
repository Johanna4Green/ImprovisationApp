# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import sys

import pygame
import pygame.midi
import time

from constants import *
from midiInput import MidiInput
from key import Key


class Window(QMainWindow):
    def __init__(self):

        super().__init__()      # exended from class QMainWindow
 
        self.title = "Improvisation App"
        self.top = WINDOW_X
        self.left = WINDOW_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT

        self.InitKeyboard(88)
        self.InitWindow()

        # timer to update the application
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(10)
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start()


    def InitWindow(self):
        #print('in InitWindow')
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def InitKeyboard(self, num_keys):
        self.keys = []
        for i in range(num_keys):
            self.keys.append(Key(i))


    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
  
        painter = QPainter(self)    # create the object of QPainter class

        #for key in self.keys:
        #    key.draw(painter)
        for key in WHITE_KEYS:
            key.draw(painter)
        for key in BLACK_KEYS:
            key.draw(painter)

        return

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
midi_input = MidiInput()
window = Window()
sys.exit(App.exec())