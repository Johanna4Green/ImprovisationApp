# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import sys
import pygame
import pygame.midi
import time
from constants import *
from midiInput import MidiInput
from backingTrack import BackingTrack
#from noteline import Noteline
from notenzeile import Notenzeile
from key import Key
import keyboard
from chord import Chord



class Window(QMainWindow):

    def __init__(self):
        print("in main Window ")
        super().__init__()      # exended from class QMainWindow
        self.title = "Improvisation App"
        self.top = WINDOW_X
        self.left = WINDOW_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT

        # init buttons, keyboard and window
        self.InitButtons()
        self.InitLabel()
        #noze.InitLabel()
        self.InitKeyboard(88)
        self.InitWindow()
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


    
    
    def InitLabel(self):
        clefLabel = QLabel(self)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(112, 132)

        time44Label = QLabel(self)
        time44Label.resize(45,95)
        #time44Pixmap = QPixmap('800px-Timesignature4-4.svg.png.webp')
        time44Pixmap = QPixmap('images/timeSign44.webp')
        time44Label.setPixmap(time44Pixmap)
        time44Label.setScaledContents(True)
        time44Label.move(165, 147)

        #flatLabel = QLabel(self)
        #flatLabel.resize(10,10)
        #flatLabel = QPixmap()
    



    def InitButtons(self):
        
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



    @pyqtSlot()
    def on_click_play(self):
        print('Play button click')
        backing_track.play_bt()

    @pyqtSlot()
    def on_click_pause(self):
        print('Pause button click')
        backing_track.pause_bt()

    @pyqtSlot()
    def on_click_stop(self):
        print('Stop button click')
        backing_track.stop_bt()
       

    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
        painter = QPainter(self)    # create the object of QPainter class
        #noze = Notenzeile(painter)
        
        # Chord(painter, chordArray, notelength, tonality, xPosition)
        #cho = Chord(painter, [1,5,13], 'HALF', 'Eb', NOTELINE_VER_X +500)

        for key in WHITE_KEYS:
            key.draw(painter)
        for key in BLACK_KEYS:
            key.draw(painter)
        noze.InitNoteLine(painter)
        return
    

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
window = Window()
noze = Notenzeile()
midi_input = MidiInput()
backing_track = BackingTrack()

sys.exit(App.exec())