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
        print('chordarray in init chord', self.chordArray)
        self.Notes = self.chord_to_SingleNotes()
        print('Notes array in init chord', self.Notes)
        #self.shift = False
        #sg = SingleNote(self.chordArray[1], self.notelength, self.tonality, self.xPosition)
        #sg.draw(self.painter)
    #noteNumber, noteLength, tonality, xPosition

    def chord_to_SingleNotes(self):
        print('in chords_to_SingleNotes')
        thisYPos = 0 
        chordAr = []
        for note in self.chordArray:
            print(note, self.notelength, self.tonality, self.xPosition)
            singlNote = SingleNote(note, self.notelength, self.tonality, self.xPosition)
            # überprüfe Überschneidung - hier reicht an dieser Stelle übrigens schon der Notenwert, weil die Halbtöne schon korrekt dargestellt werden
            yPos = singlNote.getYPos()
            #print(type(yPos))
            #print('yPos in chord:', yPos)
            #shift = False
            #if singlNote
            #singlNote.shiftRight()

            #y_pos = singlNote.calculate_note_position(singlNote.noteNumber)
            #print(type(singlNote.noteNumber))
            #print('Notennumberprintin', singlNote.noteNumber)
            #print(y_pos)
            
            if thisYPos - yPos == Y_NOTE_DISTANCE:
                print(thisYPos - yPos)
                #print('SHIFT = TRUE')
                shift = True
                print(shift)
            else:
                print(thisYPos - yPos)
                #print('SHIFT = FALSE')
                shift = False
                print(shift)
            thisYPos = yPos
            chordAr.append(singlNote)
            self.shifts[singlNote] = shift
        print(' return of chord_tp_SingleNotes', chordAr)
        return chordAr#, self.shifts[singlNote]


    def draw(self, painter):
        #self.chord_to_SingleNotes()
        #print(self.Notes)
        for singlNote in self.Notes:
            #print(singlNote.noteNumber)
            singlNote.draw(painter, self.shifts[singlNote])
            print(self.shifts[singlNote])
    
        #if self.noteLength = 'EIGHTH'
        #    for singleNot

        ###get highest note of Notes
        ###and the y position of it
        ###draw fähnchen this many pixel above it --> siehe singleNote eightLenght 
        #print('drawing the fähnchen')
        #print(self.Notes[(len(self.Notes)-1)].xPosition)
        #y_pos = self.Notes[(len(self.Notes)-1)].calculate_note_position()
        #print(y_pos)




#cho = Chord([1,5,18], 'QUARTER', 'Eb', NOTELINE_VER_X +500)
#cho.chord_to_SingleNotes()


'''
        # Chord
        Noten = []
        for event in Events:
        Noten.append(Note(event.irgendwas))             #xPos und Länge
        for note in Noten:
        if note.overlaps():
            note.rutsch_zur_seite()
'''



'''
        def draw(self, painter):
            beforeNote = 99
            for note in self.chordArray:
                print('in for loop ')
                if note == beforeNote +1 or note == beforeNote -1:
                    xPos = self.xPosition + NOTEWIDTH
                else:
                    xPos = self.xPosition

                beforeNote = note 

                #if self.xPosition == 

                #check if notes are next to each other

                #print(self.chordArray.length)
                print(note)
                singleNote = SingleNote(note, self.notelength, self.tonality, xPos)
                ###### check if note is directly next to note. HOW????? easier to do in singleNote 
                ###### check xPos from  singleNote before, if  == 15 move to 17, if == 17, stay at 15
                singleNote.draw(painter)
                #return singleNote
                #self.chord_to_SingleNotes(painter)

'''
# get chordArray from notenzeile.py
# containing several notes