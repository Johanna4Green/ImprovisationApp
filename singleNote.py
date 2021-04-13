# Noten-Klasse, die eine Tonhöhe- und Länge bekommt und daraus ein Bild einer Note macht
# je nach dem welche Länge --> Anderes Aussehen
# je nach dem welche Number --> Andere Location

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from constants import *


class SingleNote():

    def __init__(self, noteNumber, noteLength, tonality, xPosition):
        self.noteNumber = noteNumber        # 88 unterschiedl. -> 53 unterschiedl!!
        self.noteLength = noteLength        # 4 unterschied. 2.0, 1.0, 0.5, 0.25
        self.tonality = tonality
        self.xPosition = xPosition  # zum Testen: noteline1_X übergeben
        self.yPosition = NOTELINE_HOR_Y
        self.value = 'C'
        print(self.noteNumber)


    # die Notelength kann man über ein enum oder Konstanten lösen, sodass da nicht 0.5 sondern HALF steht oder so
    def draw(self, painter):

        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
           
        if self.noteLength == 'WHOLE':
            # empty circle
            painter.drawEllipse(self.xPosition, self.calculate_note_position(), NOTEWIDTH, NOTEHEIGHT)      # bobble ring
            pass
        elif self.noteLength == 'HALF':
            # empty circle with bar
            print('in HalfPrinter')
            #painter.setBrush(NoBrush)
            painter.drawEllipse(self.xPosition, self.calculate_note_position(), NOTEWIDTH, NOTEHEIGHT)      # bobble ring
            lineX = self.xPosition + NOTEWIDTH
            lineY = self.calculate_note_position() + NOTEHEIGHT/2
            painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
            pass
        elif self.noteLength == 'QUARTER':
            # filled circle with bar
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            painter.drawEllipse(self.xPosition, self.calculate_note_position(), NOTEWIDTH, NOTEHEIGHT)      # bobble filled
            lineX = self.xPosition + NOTEWIDTH
            lineY = self.calculate_note_position() + NOTEHEIGHT/2
            painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
        elif self.noteLength == 'EIGHTH':
            # filled circle with bar and tick
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            painter.drawEllipse(self.xPosition, self.calculate_note_position(), NOTEWIDTH, NOTEHEIGHT)      # booble filled
            lineX = self.xPosition + NOTEWIDTH
            lineY = self.calculate_note_position() + NOTEHEIGHT/2           
            painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
            painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX + NOTETICKLENGTH, lineY - (NOTEBARLENGTH - NOTETICKLENGTH))    # note tick
        else:
            print("error: note has impossible length")

    

    # gets yPosition for note depending of noteNumber
    # depending on sharp/ flat form sharp_or_flat function: all "black notes" are shifted up one note when sharp, shifted down one note when flat 
    def calculate_note_position(self):

        if self.number_to_value(self.noteNumber) in BLACKVALUES:
            print('in MAJMIN')
            if self.sharp_or_flat() == 'is_sharp':
                print(self.noteNumber)
                self.noteNumber = self.noteNumber + 1
                print(self.noteNumber)
                return self.getYPosition(self.number_to_value(self.noteNumber))

            elif self.sharp_or_flat() == 'is_flat':
                print(self.noteNumber)
                self.noteNumber = self.noteNumber - 1
                print(self.noteNumber)
                return self.getYPosition(self.number_to_value(self.noteNumber))
        else:
            print(self.noteNumber)
            return self.getYPosition(self.number_to_value(self.noteNumber))

    #determines if tonality is minor or major and thereby the note is flat or sharp
    def sharp_or_flat(self):
        if self.tonality in FLAT_TONALITY:
            return 'is_flat'
        elif self.tonality in SHARP_TONALITY:
            return 'is_sharp'
        else:
            print("this tonality does not exist in this application")

    # turns notNumber into the Value/ Notename
    def number_to_value(self, noteNumber):
        if self.noteNumber % 12 == 0: #
            print('in G#')
            self.value = OKTAVE[0]
        elif self.noteNumber % 12 == 1:
            print('in A')
            self.value = OKTAVE[1]
        elif self.noteNumber % 12 == 2: #
            print('in A#')
            self.value = OKTAVE[2]
            print(self.value)
        elif self.noteNumber % 12 == 3:
            print('in B')
            self.value = OKTAVE[3]
        elif self.noteNumber % 12 == 4:
            print('in C')
            self.value = OKTAVE[4]
        elif self.noteNumber % 12 == 5: #
            print('in C#')
            self.value = OKTAVE[5]
        elif self.noteNumber % 12 == 6:
            print('in D')
            self.value = OKTAVE[6]
        elif self.noteNumber % 12 == 7: #
            print('in D#')
            self.value = OKTAVE[7]
        elif self.noteNumber % 12 == 8:
            print('in E')
            self.value = OKTAVE[8]
        elif self.noteNumber % 12 == 9:
            print('in F')
            self.value = OKTAVE[9]
        elif self.noteNumber % 12 == 10: #
            print('in F#')
            self.value = OKTAVE[10]
        else: # self.noteNumber % 12 == 11:
            print('in G')
            self.value = OKTAVE[11]
        return self.value

    # for each given "White note" returns the yPosition in the sheetmusic lines
    def getYPosition(self, noteNumber):
        print(self.noteNumber)
        if self.value == 'C':#self.noteNumber in C_NOTES:
            print('in C')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 2)
        elif self.value == 'D': #self.noteNumber in D_NOTES:
            print('in D')
            self.yPosition = NOTELINE_HOR_Y + Y_NOTE_DISTANCE
        elif self.value == 'E': #self.noteNumber in E_NOTES:
            print('in E')
            self.yPosition = NOTELINE_HOR_Y
        elif self.value == 'F': # self.noteNumber in F_NOTES:
            print('in F')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 6)
        elif self.value == 'G': # self.noteNumber in G_NOTES:
            print('in G')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 5)
        elif self.value == 'A': # self.noteNumber in A_NOTES:
            print('in A')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 4)
        elif self.value == 'B': # self.noteNumber in B_NOTES:
            print('blub')
            print('in B')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 3)
        else:
            self.yPosition = NOTELINE_HOR_Y - Y_NOTE_DISTANCE
            print("error with yPosition")
        print(self.yPosition)
        return self.yPosition



#noteline1_X =  NOTELINE_VER_X - 100
#sn = SingleNote(14, 2.0, 'F#', noteline1_X)
#sn.calculate_note_position()