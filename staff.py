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
import fluidsynth
import math
from constants import * 
from songExtracting import SongExtracting
from chord import Chord

class Staff():

    song_extracting = SongExtracting()

    def __init__(self):

        self.state = 'paused'  # playing/ paused/ stopped
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)

        self.midFILE = 'AkkordeGDur.mid'
        self.songChords = self.song_extracting.getNotesOfSong(self.midFILE)
        self.tonality = self.song_extracting.getTonality(self.midFILE)

        self.xPosition = self.setXPosition()#NOTELINE_VER_X

        self.x1_hor = NOTELINE_HOR_X1
        self.x2_hor = NOTELINE_HOR_X2
        self.y1_ver = NOTELINE_VER_Y1
        self.y2_ver = NOTELINE_VER_Y2
        self.chordList = self.getChords(self.songChords)
        #print(self.xPosition)
        fileInput_thread = threading.Thread(target=self.playTrack)
        fileInput_thread.start()



    
    def getChords(self, songchords):
        listOfChords = []
        print('in getChords')
        for entry in songchords:
            #print(self.xPosition)
            #print(entry[0], entry[1], self.tonality, self.xPosition)
            listOfChords.append(Chord(entry[0], entry[1], self.tonality, self.xPosition))
            self.xPosition = self.xPosition + self.getXDistanceOfLength(entry[1])       #X_DISTANCE/2  #224  X_DISTANCE/4 für viertel 
        return listOfChords

    



    def getXDistanceOfLength(self,length):
        print(length)
        xDistance = 0
        if length == 'WHOLE':
            xDistance = X_DISTANCE
        elif length == 'HALF':
            xDistance = X_DISTANCE/2
        elif length == 'QUARTER':
            xDistance = X_DISTANCE/4
        else:
            xDistance = X_DISTANCE/8
        print(xDistance)
        return xDistance

    
    def getTimeOfLength(self, length):
        print(length)
        #print(type(length))
        time = 0
        if length == 'WHOLE':
            time = 2.0
        elif length == 'HALF':
            time = 1.0
        elif length == 'QUARTER':
            time = 0.5
        else:
            time = 0.25
        print(time)
        return time


    def playTrack(self):
        listOfChords = []
        len = 0
        print('in playTrack')
        while True:
            for entry in self.songChords:
                if self.state =="playing":
                    pass
                elif self.state == "paused":
                    while self.state == "paused":
                        time.sleep(0.5)     # as long as bt is paused, waits until play to continue
                        pass
                elif self.state == "stopped":
                    break
                else:
                    print("Bt failed")
                    ######### SET XPOSITION BACK TO BEGINNING #############
                    break
                print('entry1', entry[1])
                #len = entry[1]
                length = self.getTimeOfLength(entry[1])
                len = len + length 
                for entrada in entry[0]:
                    print(entrada)
                    self.fs.noteon(0, entrada, 60)
                time.sleep(length-0.1)
                for entrada in entry[0]:
                    self.fs.noteoff(0, entrada)
                    #self.xPosition = self.xPosition - X_DISTANCE
                time.sleep(0.1)
                print(len)
                if len % 2 == 0: 
                    print('dividebale by 2')
                    for chord in self.chordList: 
                        print('chord in listchord', len)
                        print(chord.xPosition)
                        #chord.xPosition = chord.xPosition - X_DISTANCE
                        chord.update_x_position()
                    #self.xPosition = self.xPosition - X_DISTANCE
                
        self.fs.delete()

   
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
            #print('x1',x)
            x = x + X_DISTANCE
            #print('x2',x)
        # draw chords 
        for chord in self.chordList:
            if chord.xPosition < 210 or chord.xPosition > (1120 - NOTEWIDTH):
            #print('in draw chord')
            #print(chord)
                pass
            else:
                chord.draw(painter)  



    def setXPosition(self):
        xPos = 210 #NOTELINE_VER_X
        return xPos
        


    def play_bt(self):
        self.state = "playing"
        print('playiay')
        return self.state

    def pause_bt(self):
        self.state = "paused"
        print('pausededed')
        return self.state

    def stop_bt(self):
        self.state = "stopped"
        print('stophophop')
        return self.state


    def InitLabel(self,window):

        clefLabel = QtWidgets.QLabel(window)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(65, 132)
        clefLabel.show()
        
        time44Label = QtWidgets.QLabel(window)
        time44Label.resize(45,95)
        time44Pixmap = QPixmap('images/timeSign44.webp')
        time44Label.setPixmap(time44Pixmap)
        time44Label.setScaledContents(True)
        time44Label.move(165, 147)
        time44Label.show()

        sharpLabel = QtWidgets.QLabel(window)
        sharpLabel.resize(20,30)
        sharpPixmap = QPixmap('images/sharp.png')
        sharpLabel.setPixmap(sharpPixmap)
        sharpLabel.setScaledContents(True)
        sharpLabel.move(120, 145)       #145 (G-Dur) immer + 8 bis unterstes Ais: 185
        sharpLabel.show()

        flatLabel = QtWidgets.QLabel(window)
        flatLabel.resize(20,30)
        flatPixmap = QPixmap('images/flat.png')
        flatLabel.setPixmap(flatPixmap)
        flatLabel.setScaledContents(True)
        flatLabel.move(130, 187)        #139 immer +8 bis unterstes Fes: 195
        flatLabel.show()