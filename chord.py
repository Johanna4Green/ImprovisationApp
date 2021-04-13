# Akkord-Klasse, die mehrere Noten enthält und auf Basis des "Akkord-Arrays" (notenzeile.py) erstellt wird
# die Notenzeile weiß, wo der Akkord sein soll und sagt es ihm
# und der Akkord weiß dann, wo die Note hin muss

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from constants import *
from singleNote import SingleNote

class Chord():

    def __init__(self, painter, chordArray, notelength, tonality, xPosition):
        self.painter = painter
        self.chordArray = chordArray
        self.notelength = notelength
        self.tonality = tonality
        self.xPosition = xPosition
        print(self.chordArray, self.notelength, self.tonality, self.xPosition)
        sg = SingleNote(13, self.notelength, self.tonality, self.xPosition)
        sg.draw(self.painter)
    #noteNumber, noteLength, tonality, xPosition


    '''

    def InitNoteLine(self):
        self.painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
        # horizontal lines / staves
        y = NOTELINE_HOR_Y
            #painter.setBrush(QBrush(Qt.black, Qt.SolidPattern)) # set brush to fill the key with color
        for line in range(5):
            self.painter.drawLine(NOTELINE_HOR_X1, y, NOTELINE_HOR_X2, y)
            y = y + Y_DISTANCE
            print(y)
        # vertical lines / bar line
        x = NOTELINE_VER_X
        for line in range(3):
            self.painter.drawLine(x, NOTELINE_VER_Y1, x, NOTELINE_VER_Y2)
            x = x + X_DISTANCE
        #noteline1_X =  NOTELINE_VER_X - 100
        #noteline1_Y =  NOTELINE_HOR_Y + 32
    '''

    
    # get chordArray from notenzeile.py
    # containing several notes
