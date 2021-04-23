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
        #self.painter = painter
        self.chordArray = chordArray
        self.notelength = notelength
        self.tonality = tonality
        self.xPosition = xPosition
        #print(self.chordArray, self.notelength, self.tonality, self.xPosition)
        self.shifts = {}
        #print('chordarray in init chord', self.chordArray)
        self.Notes = self.chord_to_SingleNotes()
        #print('Notes array in init chord', self.Notes)
        #self.shift = False
        #sg = SingleNote(self.chordArray[1], self.notelength, self.tonality, self.xPosition)
        #sg.draw(self.painter)
        #self.get_the_shift()
    #noteNumber, noteLength, tonality, xPosition

    def chord_to_SingleNotes(self):
        print('in chords_to_SingleNotes')
        thisYPos = 0 
        firstYPos = 0
        chordAr = []
        for note in self.chordArray:
            #print(note, self.notelength, self.tonality, self.xPosition)
            singlNote = SingleNote(note, self.notelength, self.tonality, self.xPosition)
            #self.xPosition = self.xPosition + 20
            ########## COMPARE VALUE #############
            # überprüfe Überschneidung - hier reicht an dieser Stelle übrigens schon der Notenwert, weil die Halbtöne schon korrekt dargestellt werden
            #val = singlNote.getValue()
            yPos = singlNote.getYPos()
            #print(yPos)
            #print(type(yPos))
            #print('val in chord', val)
            print('yPos in chord:', yPos)
            #shift = False
            #if singlNote
            #singlNote.shiftRight()

            #y_pos = singlNote.calculate_note_position(singlNote.noteNumber)
            #print(type(singlNote.noteNumber))
            #print('Notennumberprintin', singlNote.noteNumber)
            #print(y_pos)
            if note == self.chordArray[0]:
                print('first chord', yPos) 
                firstYPos = abs(yPos)
            print('FYP', firstYPos)
            print('FYP DIST', (yPos - firstYPos) )
            #print('DISTANCE', thisYPos - yPos)
            #print('DIST TO FIRST NOTE', thisYPos - firstYPos )
            if thisYPos - yPos == Y_NOTE_DISTANCE or abs(yPos - firstYPos) == Y_NOTE_DISTANCE:
                print('its ydist',thisYPos - yPos)
                #print('SHIFT = TRUE')
                shift = True
                print(shift)
            else:
                print('its no ydist', thisYPos - yPos)
                #print('SHIFT = FALSE')
                shift = False
                print(shift)
            thisYPos = yPos
            chordAr.append(singlNote)
            self.shifts[singlNote] = shift
        #print(' return of chord_tp_SingleNotes', chordAr)
        return chordAr#, self.shifts[singlNote]


    def get_the_shift(self):
        y = 0 
        for singleNote in self.Notes:
            yPos = singleNote.getYPos()
            print('in chord printin singNote Position', yPos)
            if yPos - y == Y_DISTANCE:
                shift = True
                #singleNote.xPosition = singleNote.xPosition + NOTEWIDTH
            else:
                shift = False
                #pass
            y = yPos
            self.shifts[singleNote] = shift
            return self.shifts[singleNote]







    def draw(self, painter):
        #self.chord_to_SingleNotes()
        #print(self.Notes)
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
        #print('in get x pos chord ')
        for sg in self.Notes:
            sg.get_x_position()
            return sg.get_x_position()

    def update_x_position(self):
        for singleNoti in self.Notes:
            singleNoti.update_x_position()