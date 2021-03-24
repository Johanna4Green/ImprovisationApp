# the keys are created and inizialized 
# gets MidiInput from the midiInput module/ class

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



class Key():

    BLACK_KEYS = [1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40 ,42, 45, 47, 49, 52, 54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85] # welche Tasten sind schwarz?
    # this array stores the x position dependent of the DISTANCE_TO_LEFT_MARGIN of all black and white keys 
    X_POSITION_ARRAY = [DISTANCE_TO_LEFT_MARGIN,DISTANCE_TO_LEFT_MARGIN + 14, DISTANCE_TO_LEFT_MARGIN + 20, DISTANCE_TO_LEFT_MARGIN + 40, DISTANCE_TO_LEFT_MARGIN + 54, DISTANCE_TO_LEFT_MARGIN + 60 , DISTANCE_TO_LEFT_MARGIN + 74 , DISTANCE_TO_LEFT_MARGIN + 80,
        DISTANCE_TO_LEFT_MARGIN + 100, DISTANCE_TO_LEFT_MARGIN + 114, DISTANCE_TO_LEFT_MARGIN + 120, DISTANCE_TO_LEFT_MARGIN + 134, DISTANCE_TO_LEFT_MARGIN + 140, DISTANCE_TO_LEFT_MARGIN + 154, DISTANCE_TO_LEFT_MARGIN + 160, DISTANCE_TO_LEFT_MARGIN + 180, DISTANCE_TO_LEFT_MARGIN + 194,
        DISTANCE_TO_LEFT_MARGIN + 200, DISTANCE_TO_LEFT_MARGIN + 214, DISTANCE_TO_LEFT_MARGIN + 220, DISTANCE_TO_LEFT_MARGIN + 240, DISTANCE_TO_LEFT_MARGIN + 254, DISTANCE_TO_LEFT_MARGIN + 260, DISTANCE_TO_LEFT_MARGIN + 274, DISTANCE_TO_LEFT_MARGIN + 280, DISTANCE_TO_LEFT_MARGIN + 294,
        DISTANCE_TO_LEFT_MARGIN + 300, DISTANCE_TO_LEFT_MARGIN + 320, DISTANCE_TO_LEFT_MARGIN + 334, DISTANCE_TO_LEFT_MARGIN + 340, DISTANCE_TO_LEFT_MARGIN + 354, DISTANCE_TO_LEFT_MARGIN + 360, DISTANCE_TO_LEFT_MARGIN + 380, DISTANCE_TO_LEFT_MARGIN + 394, 
        DISTANCE_TO_LEFT_MARGIN + 400, DISTANCE_TO_LEFT_MARGIN + 414, DISTANCE_TO_LEFT_MARGIN + 420, DISTANCE_TO_LEFT_MARGIN + 434, DISTANCE_TO_LEFT_MARGIN + 440, DISTANCE_TO_LEFT_MARGIN + 460, DISTANCE_TO_LEFT_MARGIN + 474, DISTANCE_TO_LEFT_MARGIN + 480, DISTANCE_TO_LEFT_MARGIN + 494, 
        DISTANCE_TO_LEFT_MARGIN + 500, DISTANCE_TO_LEFT_MARGIN + 520, DISTANCE_TO_LEFT_MARGIN + 534, DISTANCE_TO_LEFT_MARGIN + 540, DISTANCE_TO_LEFT_MARGIN + 554, DISTANCE_TO_LEFT_MARGIN + 560, DISTANCE_TO_LEFT_MARGIN + 574, DISTANCE_TO_LEFT_MARGIN + 580,
        DISTANCE_TO_LEFT_MARGIN + 600, DISTANCE_TO_LEFT_MARGIN + 614, DISTANCE_TO_LEFT_MARGIN + 620, DISTANCE_TO_LEFT_MARGIN + 634, DISTANCE_TO_LEFT_MARGIN + 640, DISTANCE_TO_LEFT_MARGIN + 660, DISTANCE_TO_LEFT_MARGIN + 674, DISTANCE_TO_LEFT_MARGIN + 680, DISTANCE_TO_LEFT_MARGIN + 694,
        DISTANCE_TO_LEFT_MARGIN + 700, DISTANCE_TO_LEFT_MARGIN + 714, DISTANCE_TO_LEFT_MARGIN + 720, DISTANCE_TO_LEFT_MARGIN + 740, DISTANCE_TO_LEFT_MARGIN + 754, DISTANCE_TO_LEFT_MARGIN + 760, DISTANCE_TO_LEFT_MARGIN + 774, DISTANCE_TO_LEFT_MARGIN + 780,
        DISTANCE_TO_LEFT_MARGIN + 800, DISTANCE_TO_LEFT_MARGIN + 814, DISTANCE_TO_LEFT_MARGIN + 820, DISTANCE_TO_LEFT_MARGIN + 834, DISTANCE_TO_LEFT_MARGIN + 840, DISTANCE_TO_LEFT_MARGIN + 854, DISTANCE_TO_LEFT_MARGIN + 860, DISTANCE_TO_LEFT_MARGIN + 880, DISTANCE_TO_LEFT_MARGIN + 894,
        DISTANCE_TO_LEFT_MARGIN + 900, DISTANCE_TO_LEFT_MARGIN + 914, DISTANCE_TO_LEFT_MARGIN + 920, DISTANCE_TO_LEFT_MARGIN + 940, DISTANCE_TO_LEFT_MARGIN + 954, DISTANCE_TO_LEFT_MARGIN + 960, DISTANCE_TO_LEFT_MARGIN + 974, DISTANCE_TO_LEFT_MARGIN + 980, DISTANCE_TO_LEFT_MARGIN + 994,
        DISTANCE_TO_LEFT_MARGIN + 1000, DISTANCE_TO_LEFT_MARGIN + 1020, DISTANCE_TO_LEFT_MARGIN + 1040
    ] # (16,25, 33, 42, 50, 59, 67, 76, 85 is letztes



    def __init__(self, key_number):

        super().__init__()
        self.key_number = key_number
        self.is_pressed = False

        self.x = self.X_POSITION_ARRAY[self.key_number]
        self.y = 200
        self.w = 20
        self.w_black = 12
        self.h =  170
        self.h_black = 110
        self.white_circle_w = 10
        self.black_circle_w = 8
        self.white_circle_h = 10
        self.black_circle_h = 8

        #self.painter = QPainter(self)    # reated the object of QPainter class

        if key_number in self.BLACK_KEYS:
            self.key_type = KEY_TYPE_BLACK
            BLACK_KEYS.append(self)
        else:
            self.key_type = KEY_TYPE_WHITE
            WHITE_KEYS.append(self)


    def draw(self, painter):
        is_pressed = midi_input.getKeyArray()[self.key_number]
      
        if self.key_type == KEY_TYPE_BLACK:
            # zeichne ein schwarzes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w_black, self.h_black)

            if is_pressed:
                # zeichne die Markierung
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 2, self.y + 100, self.black_circle_w, self.black_circle_h)
                pass
                
        else:
            # zeichne ein weißes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w, self.h)
            
            if is_pressed:
                # zeichne die Markierung
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 5, self.y + 155, self.white_circle_w, self.white_circle_h)
                pass
               
midi_input = MidiInput()