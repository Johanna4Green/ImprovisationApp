# Akkord-Klasse, die mehrere Noten enthält und auf Basis des "Akkord-Arrays" (staff.py) erstellt wird
# die Notenzeile/ Staff weiß, wo der Akkord sein soll und sagt es ihm
# und der Akkord weiß dann, wo die Note hin muss

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from constants import *
from singleNote import SingleNote

class Chord():

    def __init__(self, chordArray, notelength, tonality, xPosition):
        self.chordArray = chordArray
        self.notelength = notelength
        self.tonality = tonality
        self.xPosition = xPosition
        #print(self.chordArray, self.notelength, self.tonality, self.xPosition)
        self.shifts = {}
        #print('chordarray in init chord', self.chordArray)
        self.Notes = self.chord_to_SingleNotes()
        #print('Notes array in init chord', self.Notes)
       
    def chord_to_SingleNotes(self):
        #print('in chords_to_SingleNotes')
        thisYPos = 0 
        firstYPos = 0
        chordAr = []
        for note in self.chordArray:
            #print(note, self.notelength, self.tonality, self.xPosition)
            singlNote = SingleNote(note, self.notelength, self.tonality, self.xPosition)
            yPos = singlNote.getYPos()
            #print('yPos in chord:', yPos)
            if note == self.chordArray[0]:
                firstYPos = abs(yPos)
            #print('FYP', firstYPos)
            if thisYPos - yPos == Y_NOTE_DISTANCE or abs(yPos - firstYPos) == Y_NOTE_DISTANCE:
                #print('its ydist',thisYPos - yPos)
                shift = True
                #print(shift)
            else:
                #print('its no ydist', thisYPos - yPos)
                shift = False
                #print(shift)
            thisYPos = yPos
            chordAr.append(singlNote)
            self.shifts[singlNote] = shift
        return chordAr

    def draw(self, painter):
       
        for singlNote in self.Notes:
            #print(singlNote.noteNumber)
            singlNote.draw(painter, self.shifts[singlNote])
            #print(self.shifts[singlNote])
    
        #if self.noteLength = 'EIGHTH'
        #    for singleNot

        ###get highest note of Notes
        ###and the y position of it
        ###draw fähnchen this many pixel above it --> siehe singleNote eightLenght 
        #print('drawing the fähnchen')
        #print(self.Notes[(len(self.Notes)-1)].xPosition)
        #y_pos = self.Notes[(len(self.Notes)-1)].calculate_note_position()
        #print(y_pos)

    def get_x_position(self):
        for sg in self.Notes:
            sg.get_x_position()
            return sg.get_x_position()

    def update_x_position(self):
        for singleNoti in self.Notes:
            singleNoti.update_x_position()