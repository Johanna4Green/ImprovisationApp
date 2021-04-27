# chord class is containing several notes (one chord) which is created by staff.py
# staff tells chord the x_position, chord tells singleNote the x_position

from PyQt5.QtGui import QPainter, QBrush, QPen
from constants import *
from singleNote import SingleNote

class Chord():

    def __init__(self, chord_array, note_length, tonality, x_position):
        self.chord_array = chord_array
        self.note_length = note_length
        self.tonality = tonality
        self.x_position = x_position
        self.shifts = {}    # if notes are only one halftone apart, one has to be moved one notelength on the x-axis
        self.notes = self.chord_to_single_notes()   # array of singleNote instances
        

    # creating an array out of singleNote instances
    # comparing the y_positions of all the notes in the chord array to figure out, if shifitng is necessary   
    def chord_to_single_notes(self):
        last_y_pos = 0  # y_pos of note before the current 'y_pos'
        first_y_pos = 0 # y_pos of first note in array
        this_chord_array = []
        for note in self.chord_array:
            single_note = SingleNote(note, self.note_length, self.tonality, self.x_position)
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


    def draw(self, painter):
        for single_note in self.notes:
            single_note.draw(painter, self.shifts[single_note])
    
    
    def get_x_position(self):
        for single_note in self.notes:
            return single_note.get_x_position()

    def set_x_position(self, x_pos):
        for single_note in self.notes:
            single_note.set_x_position(x_pos)

    def update_x_position(self):
        for single_note in self.notes:
            single_note.update_x_position()

    def reset_x_position(self, basic_x_pos):
        for single_note in self.notes:
            single_note.reset_x_position(basic_x_pos)