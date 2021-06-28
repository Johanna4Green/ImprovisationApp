# this class creates the single note in the staff. Staff.py creates the chord, chord.py creates the singleNotes. 
# gets tonality, note_length, note_number and the x_position
# evaluates the y_position and shifts x_position if necessary

from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from constants import *


class SingleNote():

    def __init__(self, note_number, note_length, tonality, x_position):
        self.note_number = note_number        # 88 unterschiedl. -> 53 unterschiedl!!
        self.note_length = note_length        # 4 unterschied. 2.0, 1.0, 0.5, 0.25
        self.tonality = tonality
        self.x_position = x_position  # zum Testen: noteline1_X übergeben
        self.value = OKTAVE_C[self.note_number % 12]   #self.number_to_value(self.noteNumber)
        self.y_position = self.calculate_note_position()
       

    # draw note according to notelength 
    # only works for whole notes, because of the moving further in the backing track noteline, but here it's prepared for the other note values
    def draw(self, painter, shift):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # set pen to draw the outline of the key
        if self.note_length == 'WHOLE':  # empty circle
            if shift == False:
                painter.drawEllipse(self.x_position, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # bobble ring
                pass
            else: # shift == True
                shift_x_pos = self.x_position + NOTEWIDTH
                painter.drawEllipse(shift_x_pos, self.y_position, NOTEWIDTH, NOTEHEIGHT)  
                pass

        elif self.note_length == 'HALF': # empty circle with bar
            if shift == False:
                painter.drawEllipse(self.x_position, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # bobble ring
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos)                                    # note bar
                pass
            else:  # shift == True
                shift_x_pos = self.x_position + NOTEWIDTH
                painter.drawEllipse(shift_x_pos, self.y_position, NOTEWIDTH, NOTEHEIGHT) 
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos)       
                pass

        elif self.note_length == 'QUARTER': # filled circle with bar
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            if shift == False:
                painter.drawEllipse(self.x_position, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # bobble filled
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos) 
                pass
            else:  # shift == True 
                shift_x_pos = self.x_position + NOTEWIDTH
                painter.drawEllipse(shift_x_pos, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # bobble filled
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos)       
                pass

        elif self.note_length == 'EIGHTH':   # filled circle with bar and tick
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            if shift == False:
                painter.drawEllipse(self.x_position, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # booble filled
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos)        # note bar
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos + NOTETICKLENGTH, bar_y_pos - (NOTEBARLENGTH - NOTETICKLENGTH))    # note tick
            else:  # shift == True 
                shift_x_pos = self.x_position + NOTEWIDTH
                painter.drawEllipse(shift_x_pos, self.y_position, NOTEWIDTH, NOTEHEIGHT)      # booble filled
                bar_x_pos = self.x_position + NOTEWIDTH
                bar_y_pos = self.y_position + NOTEHEIGHT/2
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos, bar_y_pos)        # note bar
                painter.drawLine(bar_x_pos, bar_y_pos - NOTEBARLENGTH, bar_x_pos + NOTETICKLENGTH, bar_y_pos - (NOTEBARLENGTH - NOTETICKLENGTH))    # note tick
        else:
            print("error: note has impossible length")


    # gets y_position for note depending of note_number
    # depending on sharp/ flat form sharp_or_flat function: all "black notes" are shifted down one note when sharp, shifted up one note when flat 
    def calculate_note_position(self):
        if self.value in BLACKVALUES:
            if self.sharp_or_flat() == 'is_sharp':
                self.note_number = self.note_number - 1
                self.value = OKTAVE_C[self.note_number % 12]
                return self.get_y_position(self.value)
            elif self.sharp_or_flat() == 'is_flat':
                self.note_number = self.note_number + 1
                self.value = OKTAVE_C[self.note_number % 12]
                return self.get_y_position(self.value)
        else:
            self.value = OKTAVE_C[self.note_number % 12]
            return self.get_y_position(self.value)

    #determines if tonality is minor or major and thereby the note is flat or sharp
    def sharp_or_flat(self):
        if self.tonality in FLAT_TONALITY:
            return 'is_flat'
        elif self.tonality in SHARP_TONALITY:
            return 'is_sharp'
        else:
            print("tonality C")

   
    # for each given "White note" returns the y_position in the sheetmusic lines
    def get_y_position(self, value):
        if value == 'C':
            self.y_position = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 2)
        elif value == 'D':
            self.y_position = NOTELINE_HOR_Y + Y_NOTE_DISTANCE
        elif value == 'E':
            self.y_position = NOTELINE_HOR_Y
        elif value == 'F':
            self.y_position = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 6)
        elif value == 'G':
            self.y_position = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 5)
        elif value == 'A':
            self.y_position = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 4)
        elif value == 'B':
            self.y_position = NOTELINE_HOR_Y + (Y_NOTE_DISTANCE * 3)
        else:
            self.y_position = NOTELINE_HOR_Y - Y_NOTE_DISTANCE
            print("error with yPosition")
        return self.y_position

    def get_x_position(self):
        return self.x_position

    def set_x_position(self, x):
        self.x_position = x 

    # moving whole staff one tact to the left
    def update_x_position(self):
        self.x_position = self.x_position - X_DISTANCE      

    def get_y_pos(self): 
        return self.y_position

    def reset_x_position(self, basic_x_pos):
        self.x_position = basic_x_pos