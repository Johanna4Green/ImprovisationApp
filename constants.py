# collection of all global variables

# for drawing the keys correctly: filled in Key.py and used in gui.py
BLACK_KEYS = []
WHITE_KEYS = []
# for appending key to the correct array above, used in key.py
KEY_TYPE_BLACK = 0
KEY_TYPE_WHITE = 1

WINDOW_X = 10
WINDOW_Y = 10
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

DISTANCE_TO_LEFT_MARGIN = 100


# ONE OKTAVE starting with G# because A is the number1 note on the piano and therefore G# is 0 
OKTAVE = ['G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']
BLACKVALUES = ['C#', 'D#', 'F#', 'G#', 'A#']
# SHARP OR FLAT
FLAT_TONALITY = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb'] # f b es as des ges
SHARP_TONALITY = ['G', 'D', 'A', 'E', 'B', 'F#']   # g d a e h fis

'''
class Notelength(Enum):
    0.25 = EIGHTH
    0.5 = QUARTER
    1.0 = HALF
    2.0 = WHOLE
'''

NOTEBARLENGTH = 40
NOTETICKLENGTH = 8

NOTEWIDTH = 17
NOTEHEIGHT = 16


LINES = []
NOTES = []


# Noteline
NOTELINE_HOR_X1 = 200
NOTELINE_HOR_X2 = WINDOW_WIDTH - NOTELINE_HOR_X1
NOTELINE_HOR_Y = 160    # 176, 192, 208, 224
Y_DISTANCE = 16
Y_NOTE_DISTANCE = 8


NOTELINE_VER_X = 400 # 600, 800
NOTELINE_VER_Y1 = NOTELINE_HOR_Y
NOTELINE_VER_Y2 = NOTELINE_HOR_Y + (4*16)
X_DISTANCE = 200