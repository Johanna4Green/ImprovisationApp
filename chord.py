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

    def __init__(self, chordArray, notelength, tonality, xPosition):
        #self.painter = painter
        self.chordArray = chordArray
        self.notelength = notelength
        self.tonality = tonality
        self.xPosition = xPosition
        print(self.chordArray, self.notelength, self.tonality, self.xPosition)
        sg = SingleNote(13, self.notelength, self.tonality, self.xPosition)
        sg.draw(self.painter)
    #noteNumber, noteLength, tonality, xPosition
    
    # get chordArray from notenzeile.py
    # containing several notes
