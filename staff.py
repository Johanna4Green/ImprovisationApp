# die Notenzeile zeichnet Linien, Notenschlüssel etc und hat Instanzen der Noten-Klasse
# die Noten-Klasse kümmert sich darum, dass die Note gezeichnet wird
# der Backing-Track kann auch so ein Array haben wie der Input
# aber vermutlich musst den Backing Track extra einmal komplett auslesen für die Notenzeile, 
# sonst können die "zukünftigen" Noten ja erst gezeichnet werden, wenn sie abgespielt werden

# <meta message time_signature>
# numerator=4 denominator=4 means 4/4 Takt
# clocks_per_click=24 means that the metronome will click once every 24 MIDI clocks. 
# notated_32nd_notes_per_beat=8 means that there are eight 32nd notes per beat.

# Notenzeile, die sich um das "drumherum" wie Linien und Notenschlüssel kümmert 
# UND mehrere Akkorde enthält, die dann gezeichnet werden
# die Notenzeile weiß, wo der Akkord sein soll und sagt es ihm (und der Akkord weiß dann, wo die Note hin muss)
# "Hauptklasse" des Programms (GUI) erstellt eine neue Instanz der Notenzeile

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import time
import threading
import mido
from mido import MidiFile
from mido import MetaMessage
import math
from constants import * 
from songExtracting import SongExtracting
from chord import Chord


class Staff():

    song_extracting = SongExtracting()

    def __init__(self):
        self.midFILE = 'AkkordeGDur.mid'
        self.songChords = self.song_extracting.getNotesOfSong(self.midFILE)
        self.tonality = self.song_extracting.getTonality(self.midFILE)
        self.xPosition = self.setXPosition()#NOTELINE_VER_X
        self.x1_hor = NOTELINE_HOR_X1
        self.x2_hor = NOTELINE_HOR_X2
        self.y1_ver = NOTELINE_VER_Y1
        self.y2_ver = NOTELINE_VER_Y2
        self.chordList = self.getChords(self.songChords)
        #print(self.tonality)
        #print(self.songChords)
        #print(self.chordList)
        #print(self.xPosition)

    
    def getChords(self, songchords):
        listOfChords = []
        print('in getChords')
        for entry in songchords:
            #print(entry)
            #print(entry[0])
            #print(self.xPosition)
            print(entry[0], entry[1], self.tonality, self.xPosition)
            listOfChords.append(Chord(entry[0], entry[1], self.tonality, self.xPosition))
            self.xPosition = self.xPosition + 50
        #print(self.chordList)
        #print(len(listOfChords))
        return listOfChords
        

    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # set pen to draw the outline of the key
        # horizontal lines / staves
        y = NOTELINE_HOR_Y
        for line in range(5):
            painter.drawLine(self.x1_hor, y, self.x2_hor, y)
            y = y + Y_DISTANCE
        # vertical lines / bar line
        x = NOTELINE_VER_X
        for line in range(3):
            painter.drawLine(x, self.y1_ver, x, self.y2_ver)
            x = x + X_DISTANCE
    # draw chords 
        for chord in self.chordList:
            #print('in draw chord')
            #print(chord)
            chord.draw(painter)
        

    def setXPosition(self):
        xPos = 450 #NOTELINE_VER_X
        return xPos
        

    def InitLabel(self,window):
        #print("in init label Notenzeile")
        
        clefLabel = QtWidgets.QLabel(window)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(112, 132)
        clefLabel.show()
        
        time44Label = QtWidgets.QLabel(window)
        time44Label.resize(45,95)
        time44Pixmap = QPixmap('images/timeSign44.webp')
        time44Label.setPixmap(time44Pixmap)
        time44Label.setScaledContents(True)
        time44Label.move(165, 147)
        time44Label.show()

        ######## NEED TO GET TONALITY AND DEPENDING ON IT SET SHARPS OR FLATS ###############################
        #flatLabel = QLabel(self)
        #flatLabel.resize(10,10)
        #flatLabel = QPixmap()