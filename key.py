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
from staff import Staff
from songExtracting import SongExtracting

class Key():

    BLACK_KEYS = [1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40 ,42, 45, 47, 49, 52, 54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85] # welche Tasten sind schwarz?

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

    def __init__(self, key_number, staff):
        super().__init__()
        self.staff = staff
        self.key_number = key_number
        self.is_pressed = False
        self.is_played_by_bt = False
        self.x = self.X_POSITION_ARRAY[self.key_number]
        self.y = 350                    # WINDOW_HEIGHT / 2  # 200
        self.w = 20                     # WINDOW_WIDTH / 60 # 20      # 52 white keys, je 4 am rand frei
        self.w_black = 12
        self.h =  170                   # w * 4 # 170
        self.h_black = 110
        self.white_circle_w = 10
        self.black_circle_w = 8
        self.white_circle_h = 10
        self.black_circle_h = 8
        self.tonality = song_extracting.getTonality(MIDIFILE)
        print('in key', self.tonality)

        if key_number in self.BLACK_KEYS:
            self.key_type = KEY_TYPE_BLACK
            BLACK_KEYS.append(self)
        else:
            self.key_type = KEY_TYPE_WHITE
            WHITE_KEYS.append(self)
        

    def getColorArray(self):
        color_ar = []
        g = [0, 2, 3, 5, 7, 9, 10]
        if self.tonality == 'G':
            for key_number in range(88):
                if key_number % 12 in g: 
                    color_ar.append(True)
                else:
                    color_ar.append(False)
               # self.key_type = KEY_TYPE_YELLOW
        else:
            print('fail in colorgetting')
        return color_ar



        #g  = 1,3,4,6,8,10,11
        #['G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']


    def draw(self, painter):

        is_pressed = midi_input.getKeyArray()[self.key_number]
        is_played_by_bt = self.staff.get_bt_keyArray()[self.key_number]
        is_colored = self.getColorArray()[self.key_number]

        # zeiche Taste
        if self.key_type == KEY_TYPE_BLACK:
            # zeichne ein schwarzes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            if is_colored:
                painter.setBrush(QBrush(Qt.darkYellow, Qt.SolidPattern)) # set brush to fill the key with color
            else:
                painter.setBrush(QBrush(Qt.black, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w_black, self.h_black)
            # zeichne die Markierung
            if is_pressed:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 2, self.y + 100, self.black_circle_w, self.black_circle_h)
            if is_played_by_bt:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 2, self.y + 100, self.black_circle_w, self.black_circle_h)
            
        else:
            # zeichne ein weißes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            if is_colored:
                painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern)) # set brush to fill the key with color
            else:
                painter.setBrush(QBrush(Qt.white, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w, self.h)
            # zeichne die Markierung
            if is_pressed:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 5, self.y + 155, self.white_circle_w, self.white_circle_h)
            if is_played_by_bt:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 5, self.y + 155, self.white_circle_w, self.white_circle_h)
                
midi_input = MidiInput()
song_extracting = SongExtracting()
#staf = Staff()
