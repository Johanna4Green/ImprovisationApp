# chord class is containing several notes (one chord) which is created by staff.py
# staff tells chord the x_position, chord tells singleNote the x_position

from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt

import music21
from music21 import stream
from music21 import note
from constants import *
from singleNote import SingleNote
from font import os_font


class Chord():

    def __init__(self, chord_array, note_length, tonality, x_position):
        self.chord_array = chord_array
        self.note_length = note_length
        self.tonality = tonality
        self.x_position = x_position
        self.shifts = {}    # if notes are only one halftone apart, one has to be moved one notelength on the x-axis
        self.notes = self.chord_to_single_notes()   # array of singleNote instances
        self.chord_symbol = self.create_chord_symbol()
        #print('chord_symbol in init', self.chord_symbol)
        

    # creating an array out of singleNote instances
    # comparing the y_positions of all the notes in the chord array to figure out, if shifitng is necessary   
    def chord_to_single_notes(self):
        last_y_pos = 0  # y_pos of note before the current 'y_pos'
        first_y_pos = 0 # y_pos of first note in array
        this_chord_array = []
        for note in self.chord_array:
            single_note = SingleNote(note, self.note_length, self.tonality, self.x_position)
            #print(single_note.value)
            #print('oktave', OKTAVE_C[note % 12])
            current_y_pos = single_note.get_y_pos() # y_pos of current note
            if note == self.chord_array[0]:
                first_y_pos = abs(current_y_pos)
            if last_y_pos - current_y_pos == Y_NOTE_DISTANCE or abs(current_y_pos - first_y_pos) == Y_NOTE_DISTANCE:
                shift = True
            else:
                shift = False
            last_y_pos = current_y_pos
            this_chord_array.append(single_note)
            self.shifts[single_note] = shift
        return this_chord_array


    # creating the chord symbol text with 'Krumhansl' from music21 
    def create_chord_symbol(self):
        chord_stream = stream.Stream()
        for note_number in self.chord_array:
            note_name = OKTAVE_C[note_number % 12]
            #print('oktave', note_name)
            chord_stream.append(note.Note(note_name))
        #print(len(chord_stream))
        chord_symbol = chord_stream.analyze('Krumhansl')
        chord_tonic_name = chord_symbol.tonic.name
        chord_mode = chord_symbol.mode
        if chord_mode == 'minor':
            written_chord_mode = 'm'
        elif chord_mode == 'major':
            written_chord_mode = ''
        written_chord = chord_tonic_name + written_chord_mode
        #print(chord_tonic_name, chord_mode)
        return written_chord



    # write the created chord symbol above the chord
    def drawText(self, painter):
        text = self.chord_symbol
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setFont(QFont(os_font, 20))        #QFont('Skia',20)) #  Helvetica  Arial
        x_pos = self.x_position
        y_pos = 120
        w = 50
        h = 20
        text_align = Qt.AlignLeft
        painter.drawText(x_pos, y_pos, w, h, text_align, text)


    # draw each note of the chord by calling the drawing function from singleNote
    def draw(self, painter):
        self.drawText(painter)
        for single_note in self.notes:
            single_note.draw(painter, self.shifts[single_note])
    
    
    def get_x_position(self):
        for single_note in self.notes:
            return single_note.get_x_position()

    def set_x_position(self, x_pos):
        self.x_position = x_pos
        for single_note in self.notes:
            single_note.set_x_position(x_pos)

    def update_x_position(self):
        self.x_position = self.x_position - X_DISTANCE
        for single_note in self.notes:
            single_note.update_x_position()

    def reset_x_position(self, basic_x_pos):
        self.x_position = basic_x_pos
        for single_note in self.notes:
            single_note.reset_x_position(basic_x_pos)

    def get_chord_symbol(self):
        return self.chord_symbol