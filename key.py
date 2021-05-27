# this class draws the keys of the keyboard. 
# It also draws the red dots on top as current feedback (info gotten from midiInput thread).
# It also draws the blue dots on top as visualization of the chords played by the Backing Track
# (info gotten from staff thread).
# It also colors the keys of the keyboard depending on the tonality to show possible play material
# (info gotten from songExtracting).

from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

from constants import *
from midiInput import MidiInput
from songExtracting import SongExtracting

class Key():

    BLACK_KEYS = [1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40 ,42, 45, 47, 49, 52, 54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85] # welche Tasten sind schwarz?

    X_POSITION_ARRAY = [ORIG_KEY_X_POS,ORIG_KEY_X_POS + 14, ORIG_KEY_X_POS + 20, ORIG_KEY_X_POS + 40, ORIG_KEY_X_POS + 54, ORIG_KEY_X_POS + 60 , ORIG_KEY_X_POS + 74 , ORIG_KEY_X_POS + 80,
                        ORIG_KEY_X_POS + 100, ORIG_KEY_X_POS + 114, ORIG_KEY_X_POS + 120, ORIG_KEY_X_POS + 134, ORIG_KEY_X_POS + 140, ORIG_KEY_X_POS + 154, ORIG_KEY_X_POS + 160, ORIG_KEY_X_POS + 180, ORIG_KEY_X_POS + 194,
                        ORIG_KEY_X_POS + 200, ORIG_KEY_X_POS + 214, ORIG_KEY_X_POS + 220, ORIG_KEY_X_POS + 240, ORIG_KEY_X_POS + 254, ORIG_KEY_X_POS + 260, ORIG_KEY_X_POS + 274, ORIG_KEY_X_POS + 280, ORIG_KEY_X_POS + 294,
                        ORIG_KEY_X_POS + 300, ORIG_KEY_X_POS + 320, ORIG_KEY_X_POS + 334, ORIG_KEY_X_POS + 340, ORIG_KEY_X_POS + 354, ORIG_KEY_X_POS + 360, ORIG_KEY_X_POS + 380, ORIG_KEY_X_POS + 394, 
                        ORIG_KEY_X_POS + 400, ORIG_KEY_X_POS + 414, ORIG_KEY_X_POS + 420, ORIG_KEY_X_POS + 434, ORIG_KEY_X_POS + 440, ORIG_KEY_X_POS + 460, ORIG_KEY_X_POS + 474, ORIG_KEY_X_POS + 480, ORIG_KEY_X_POS + 494, 
                        ORIG_KEY_X_POS + 500, ORIG_KEY_X_POS + 520, ORIG_KEY_X_POS + 534, ORIG_KEY_X_POS + 540, ORIG_KEY_X_POS + 554, ORIG_KEY_X_POS + 560, ORIG_KEY_X_POS + 574, ORIG_KEY_X_POS + 580,
                        ORIG_KEY_X_POS + 600, ORIG_KEY_X_POS + 614, ORIG_KEY_X_POS + 620, ORIG_KEY_X_POS + 634, ORIG_KEY_X_POS + 640, ORIG_KEY_X_POS + 660, ORIG_KEY_X_POS + 674, ORIG_KEY_X_POS + 680, ORIG_KEY_X_POS + 694,
                        ORIG_KEY_X_POS + 700, ORIG_KEY_X_POS + 714, ORIG_KEY_X_POS + 720, ORIG_KEY_X_POS + 740, ORIG_KEY_X_POS + 754, ORIG_KEY_X_POS + 760, ORIG_KEY_X_POS + 774, ORIG_KEY_X_POS + 780,
                        ORIG_KEY_X_POS + 800, ORIG_KEY_X_POS + 814, ORIG_KEY_X_POS + 820, ORIG_KEY_X_POS + 834, ORIG_KEY_X_POS + 840, ORIG_KEY_X_POS + 854, ORIG_KEY_X_POS + 860, ORIG_KEY_X_POS + 880, ORIG_KEY_X_POS + 894,
                        ORIG_KEY_X_POS + 900, ORIG_KEY_X_POS + 914, ORIG_KEY_X_POS + 920, ORIG_KEY_X_POS + 940, ORIG_KEY_X_POS + 954, ORIG_KEY_X_POS + 960, ORIG_KEY_X_POS + 974, ORIG_KEY_X_POS + 980, ORIG_KEY_X_POS + 994,
                        ORIG_KEY_X_POS + 1000, ORIG_KEY_X_POS + 1020, ORIG_KEY_X_POS + 1040
                        ] # (16,25, 33, 42, 50, 59, 67, 76, 85 is letztes

    def __init__(self, key_number, staff):
        super().__init__()
        self.midifile = MIDIFILE
        self.staff = staff
        self.key_number = key_number
        self.is_pressed = False
        self.is_played_by_bt = False
        self.x = self.X_POSITION_ARRAY[self.key_number]
        self.y = 350                    # WINDOW_HEIGHT / 2  # 200
        self.w = 20                     # WINDOW_WIDTH / 60 # 20      # 52 white keys, je 4 am rand frei
        self.w_black = 12
        self.h =  170                   # w * 4 # 170
        self.h_black = 110
        self.white_circle_w = 10
        self.black_circle_w = 8
        self.white_circle_h = 10
        self.black_circle_h = 8
        self.tonality = song_extracting.getTonality(self.midifile)
        print(self.midifile)

        if key_number in self.BLACK_KEYS:
            self.key_type = KEY_TYPE_BLACK
            BLACK_KEYS.append(self)
        else:
            self.key_type = KEY_TYPE_WHITE
            WHITE_KEYS.append(self)

    ################## RESET ################
    def reset_key_class(self, midifile):
        self.midifile = midifile
        self.tonality = song_extracting.getTonality(self.midifile)
    ##########################################

   
    # draws the keys (the whole keyboard) and also 
    # draws the dots for live feedback from input and backing track
    def draw(self, painter):

        is_pressed = midi_input.getKeyArray()[self.key_number]
        is_played_by_bt = self.staff.get_bt_key_array()[self.key_number]
        is_colored = self.getColorArray()[self.key_number]

        # zeiche Taste
        if self.key_type == KEY_TYPE_BLACK:
            # zeichne ein schwarzes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            if is_colored:
                painter.setBrush(QBrush(Qt.darkYellow, Qt.SolidPattern)) # set brush to fill the key with color
            else:
                painter.setBrush(QBrush(Qt.black, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w_black, self.h_black)
            # zeichne die Markierung
            if is_played_by_bt:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 2, self.y + 100, self.black_circle_w, self.black_circle_h)
            if is_pressed:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 2, self.y + 100, self.black_circle_w, self.black_circle_h)
           
        else:
            # zeichne ein weißes Viereck
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            if is_colored:
                painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern)) # set brush to fill the key with color
            else:
                painter.setBrush(QBrush(Qt.white, Qt.SolidPattern)) # set brush to fill the key with color
            painter.drawRect(self.x, self.y, self.w, self.h)
            # zeichne die Markierung
            if is_played_by_bt:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 5, self.y + 155, self.white_circle_w, self.white_circle_h)
            if is_pressed:  # or is_played_by_bt:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
                painter.drawEllipse(self.x + 5, self.y + 155, self.white_circle_w, self.white_circle_h)
          
    # depending on the tonality the notes to be colored are chosen 
    def getColorArray(self):
        #[ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
        color_array = []
        c_dur_notes = [0, 2, 3, 5, 7, 8, 10]
        g_dur_notes = [0, 2, 3, 5, 7, 9, 10]  #fis
        d_dur_notes = [0, 2, 4, 5, 7, 9, 10]  #cis
        a_dur_notes = [0, 2, 4, 5, 7, 9, 11]  #gis
        e_dur_notes = [0, 2, 4, 6, 7, 9, 11]  #dis
        b_dur_notes = [1, 2, 4, 6, 7, 9, 11]  #ais
        fis_dur_notes = [1, 2, 4, 6, 8, 9, 11] #eis 
        f_dur_notes = [0, 1, 3, 5, 7, 8, 10]    #b
        bb_dur_notes = [0, 1, 3, 5, 6, 8, 10]  #es
        es_dur_notes = [1, 3, 5, 6, 8, 10, 11]  #as
        as_dur_notes = [1, 3, 4, 6, 8, 10, 11]  #des
        des_dur_notes = [1, 3, 4, 6, 8, 9, 11]  #ges
        ges_dur_notes = [1, 2, 4, 6, 8, 9, 11]  #ces

        if self.tonality == 'C':
            ar = c_dur_notes
        elif self.tonality == 'G':
            ar = g_dur_notes
        elif self.tonality == 'D':
            ar = d_dur_notes
        elif self.tonality == 'A':
            ar = a_dur_notes
        elif self.tonality == 'E':
            ar = e_dur_notes
        elif self.tonality == 'B':
            ar = b_dur_notes
        elif self.tonality == 'F#':
            ar = fis_dur_notes
        elif self.tonality == 'F':
            ar = f_dur_notes
        elif self.tonality == 'Bb':
            ar = bb_dur_notes
        elif self.tonality == 'Eb':
            ar = es_dur_notes
        elif self.tonality == 'Ab':
            ar = as_dur_notes
        elif self.tonality == 'Db':
            ar = des_dur_notes
        elif self.tonality == 'Gb':
            ar = ges_dur_notes

        for key_number in range(88):
            if key_number % 12 in ar: 
                color_array.append(True)
            else:
                color_array.append(False)
        return color_array


midi_input = MidiInput()
song_extracting = SongExtracting()
