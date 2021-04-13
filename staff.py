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

import mido
from mido import MidiFile
from mido import MetaMessage
import math

from constants import * 
from chord import Chord


class Staff():

    def __init__(self):
        self.midFILE = 'AkkordeGDur.mid'
        self.noteArray = []
        self.overallTime = 0
        self.notelength = 'WHOLE'
        self.tonality = 'C'
        self.tones = {} # if notes start and end at different times, an array with the length is not possible, each notelength needs to be saved individually then

        # Chord(painter, chordArray, notelength, tonality, xPosition)
        #cho = Chord(painter, [1,5,13], 'HALF', 'Eb', NOTELINE_VER_X +500)



    def InitNoteLine(self, painter):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # set pen to draw the outline of the key
        # horizontal lines / staves
        y = NOTELINE_HOR_Y
        for line in range(5):
            painter.drawLine(NOTELINE_HOR_X1, y, NOTELINE_HOR_X2, y)
            y = y + Y_DISTANCE
        # vertical lines / bar line
        x = NOTELINE_VER_X
        for line in range(3):
            painter.drawLine(x, NOTELINE_VER_Y1, x, NOTELINE_VER_Y2)
            x = x + X_DISTANCE
        pass

    
    def InitLabel(self, window):
        print("in init label Notenzeile")
        
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

        #flatLabel = QLabel(self)
        #flatLabel.resize(10,10)
        #flatLabel = QPixmap()
        



    def getNotesOfSong(self):
        #self.overallTime = 0.10104166666666667  # WholeNote before
        #self.overallTime = 0.051041666666666666 # HalfNote before
        #self.overallTime = 0.026041666666666668 # QuarterNote before
        #self.overallTime = 0.013541666666666667 # EighthNote before
        #0.007291666666666667
        for msg in MidiFile(self.midFILE):
            if(msg.type != 'program_change' and msg.type != 'control_change') and not msg.is_meta:
                #print(msg)
                # calculate time since start
                self.overallTime = self.overallTime + msg.time

                if(msg.velocity > 0): # noteon
                    self.noteArray.append(msg.note)
                    # self.tones[msg.note] = self.overallTime
        
                else:  # noteoff
                    if (msg.time != 0):
                        # calculate length of this tone
                        self.notelength = self.determineLength(msg.time)
                        # self.notelength = vartime - tones[msg.note] 
                        #self.overallTime = math.ceil(self.overallTime + msg.time)

                        print(self.noteArray, self.notelength, self.overallTime) #################### THIS IMPORTANT
                        self.noteArray =[]
                    pass

  
    def determineLength(self, number):
        div = 1000000   # 1 second has 1 million microseconds
        tempo = 500000  # 1 beat has 500 thousand microseconds
        quarter = tempo/div
        if number > 2*quarter*1.05:             # the number is greater than a half note + 5% => whole note
            self.notelength = 'WHOLE'     
        elif number > quarter*1.05:             # the number is greater than a quarter note + 5% => half note 
            self.notelength = 'HALF'
        elif number > 0.5*quarter*1.05:         # the number is greater than an eighth note + 5% => quarter note
            self.notelength = 'QUARTER'
        elif number > 0.25*quarter*1.05:        # the number is greater than an sixteenth note + 5% => eighth note
            self.notelength = 'EIGHTH'
        elif number > 0.125*quarter*1.05:        # the number is greater than an thirtysecond note + 5% => eighth note
            length = 'SIXTHEENTH'
        else:
            print("ERROR in calculation")
        return self.notelength




    def getTempo(self, midfile):

        for msg in MidiFile(midfile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    print(msg.tempo)
                    self.tempo = msg.tempo
                    return self.tempo


    def getTonality(self, midfile):
        for msg in MidiFile(midfile):
            if msg.is_meta:
                if msg.type == 'key_signature':
                    #print(msg.tempo)
                    self.tonality = msg.key
                    print(self.tonality)
                    return self.tonality
                    
    
    
    def sharp_or_flat(self, tonality):
        semitone = ''
        if tonality in FLAT_TONALITY:
            semitone = 'is_flat'
        elif tonality in SHARP_TONALITY:
            semitone = 'is_sharp'
        else:
            ("this tonality does not exist in this application")
            semitone = ''
        return semitone


#nz = Notenzeile()
#nz.getNotesOfSong()
#g = nz.getTonality('sound_midis/bes.mid')
#q =nz.sharp_or_flat(g)
#print(q)

