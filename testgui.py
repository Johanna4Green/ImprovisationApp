# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this class draws a piano with 88 keys with PyQt5

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
import pygame
import pygame.midi
import time
from constants import *
#from midiInput import MidiInput
from testMidiInput import MidiInput
from key import Key
#from fluidSynther import FluidSynther


class Window(QMainWindow):
    def __init__(self):
        
        super().__init__()      # exended from class QMainWindow
        self.title = "Improvisation App"
        self.top = WINDOW_X
        self.left = WINDOW_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        # init keyboard and window
        self.InitKeyboard(88)
        self.InitWindow()
        #=================NEW
        #self.InitSoundForInput()
        # timer to update the application
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(10)
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def InitKeyboard(self, num_keys):
        self.keys = []
        for i in range(num_keys):
            self.keys.append(Key(i))

    #=================NEW
    #def InitSoundForInput(self):
    #    self.fl = FluidSynther()


    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
        print("inPaintEvent gui")
        painter = QPainter(self)    # create the object of QPainter class
        for key in WHITE_KEYS:
            key.draw(painter)
        for key in BLACK_KEYS:
            key.draw(painter)
        return

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
#fl = FluidSynther()
midi_input = MidiInput()
window = Window()
sys.exit(App.exec())