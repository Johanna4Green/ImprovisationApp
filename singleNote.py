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
        self.value = OKTAVE[self.noteNumber % 12]   #self.number_to_value(self.noteNumber)
        #self.shift = shift
        self.yPosition = self.calculate_note_position()
        #print('init singleNote', self.yPosition)
    
        #if self.noteLength == 'WHOLE' or self.noteLength == 'HALF':
        #    self.fill = Qt.SolidLine
        #else:
        #    self.fill = Qt.SolidPattern
        #print('in init')
        #print(self.noteNumber, self.noteLength, self. tonality, self.yPosition)
        #print(self.value)
        #print(self.noteNumber)





    # die Notelength kann man über ein enum oder Konstanten lösen, sodass da nicht 0.5 sondern HALF steht oder so
    def draw(self, painter, shift):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # set pen to draw the outline of the key
        if self.noteLength == 'WHOLE':  # empty circle
            if shift == False:
                painter.drawEllipse(self.xPosition, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # bobble ring
                pass
            else: # shift == True
                xPos = self.xPosition + NOTEWIDTH
                painter.drawEllipse(xPos, self.yPosition, NOTEWIDTH, NOTEHEIGHT)  
                pass

        elif self.noteLength == 'HALF': # empty circle with bar
            print('in HalfPrinter')
            if shift == False:
                painter.drawEllipse(self.xPosition, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # bobble ring
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
                pass
            else:  # shift == True
                xPos = self.xPosition + NOTEWIDTH
                painter.drawEllipse(xPos, self.yPosition, NOTEWIDTH, NOTEHEIGHT) 
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)        
                pass

        elif self.noteLength == 'QUARTER': # filled circle with bar
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            if shift == False:
                painter.drawEllipse(self.xPosition, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # bobble filled
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)
                pass
            else:  # shift == True 
                xPos = self.xPosition + NOTEWIDTH
                painter.drawEllipse(xPos, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # bobble filled
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)
                pass


        elif self.noteLength == 'EIGHTH':   # filled circle with bar and tick
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

            if shift == False:
                painter.drawEllipse(self.xPosition, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # booble filled
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2           
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX + NOTETICKLENGTH, lineY - (NOTEBARLENGTH - NOTETICKLENGTH))    # note tick
            else:  # shift == True 
                xPos = self.xPosition + NOTEWIDTH
                painter.drawEllipse(xPos, self.yPosition, NOTEWIDTH, NOTEHEIGHT)      # booble filled
                lineX = self.xPosition + NOTEWIDTH
                lineY = self.yPosition + NOTEHEIGHT/2           
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX, lineY)                                    # note bar
                painter.drawLine(lineX, lineY - NOTEBARLENGTH, lineX + NOTETICKLENGTH, lineY - (NOTEBARLENGTH - NOTETICKLENGTH))    # note tick 
        
        else:
            print("error: note has impossible length")


    # gets yPosition for note depending of noteNumber
    # depending on sharp/ flat form sharp_or_flat function: all "black notes" are shifted up one note when sharp, shifted down one note when flat 
    def calculate_note_position(self):

        if self.value in BLACKVALUES:
            #print('in MAJMIN')
            if self.sharp_or_flat() == 'is_sharp':
                #print(self.noteNumber)
                self.noteNumber = self.noteNumber + 1
                #print(self.noteNumber)
                return self.getYPosition(self.noteNumber)

            elif self.sharp_or_flat() == 'is_flat':
                #print(self.noteNumber)
                self.noteNumber = self.noteNumber - 1
                #print(self.noteNumber)
                return self.getYPosition(self.noteNumber)
        else:
            #print(self.noteNumber)
            return self.getYPosition(self.noteNumber)

    #determines if tonality is minor or major and thereby the note is flat or sharp
    def sharp_or_flat(self):
        if self.tonality in FLAT_TONALITY:
            return 'is_flat'
        elif self.tonality in SHARP_TONALITY:
            return 'is_sharp'
        else:
            print("probably tonality C or inexistent")

   
    # for each given "White note" returns the yPosition in the sheetmusic lines
    def getYPosition(self, noteNumber):
        #print(self.noteNumber)
        if self.value == 'C':#self.noteNumber in C_NOTES:
            #print('in C')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 2)
        elif self.value == 'D': #self.noteNumber in D_NOTES:
            #print('in D')
            self.yPosition = NOTELINE_HOR_Y + Y_NOTE_DISTANCE
        elif self.value == 'E': #self.noteNumber in E_NOTES:
            #print('in E')
            self.yPosition = NOTELINE_HOR_Y
        elif self.value == 'F': # self.noteNumber in F_NOTES:
            #print('in F')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 6)
        elif self.value == 'G': # self.noteNumber in G_NOTES:
            #print('in G')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 5)
        elif self.value == 'A': # self.noteNumber in A_NOTES:
            #print('in A')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 4)
        elif self.value == 'B': # self.noteNumber in B_NOTES:
            #print('in B')
            self.yPosition = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 3)
        else:
            self.yPosition = NOTELINE_HOR_Y - Y_NOTE_DISTANCE
            #print("error with yPosition")
        #print(self.yPosition)
        return self.yPosition


    def getYPos(self):
        #print(type(self.yPosition))
        return self.yPosition



