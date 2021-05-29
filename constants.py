#WINDOW
WINDOW_UPPER_LEFT_X = 10
WINDOW_UPPER_LEFT_Y = 10
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# for drawing the keys correctly: filled in Key.py and used in gui.py
BLACK_KEYS = []
WHITE_KEYS = []
# for appending key to the correct array above, used in key.py
KEY_TYPE_BLACK = 0
KEY_TYPE_WHITE = 1

# ONE OKTAVE starting with G# because A is the number1 note on the piano and therefore G# is 0 
OKTAVE = ['G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']
OKTAVE_C = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
BLACKVALUES = ['C#', 'D#', 'F#', 'G#', 'A#']
# SHARP OR FLAT
FLAT_TONALITY = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb'] # f b es as des ges
SHARP_TONALITY = ['G', 'D', 'A', 'E', 'B', 'F#']   # g d a e h fis

# for drawing notes in singleNote.py
NOTEBARLENGTH = 40
NOTETICKLENGTH = 8

NOTEWIDTH = 17
NOTEHEIGHT = 16

# to define the position of the keys in key.py
ORIG_KEY_X_POS = 80

# Noteline
LINES = []
NOTES = []

NOTELINE_HOR_X1 = 80 #125
NOTELINE_HOR_X2 = 1120#WINDOW_WIDTH - NOTELINE_HOR_X1
NOTELINE_HOR_Y = 160    # 176, 192, 208, 224
Y_DISTANCE = 16
Y_NOTE_DISTANCE = 8

NOTELINE_VER_X = 430#420 #400    # 625, 850, (beginn 125,  1st: 275, 2nd, 3rd, 4th: 225 end: 1075)  --> 50 vor Beginning                # 350, 600, 850                #400, 600, 800
NOTELINE_VER_Y1 = NOTELINE_HOR_Y
NOTELINE_VER_Y2 = NOTELINE_HOR_Y + (4*16)
X_DISTANCE = 230   #224 # 225

MIDIFILE = 'sound_midis/ADur.mid'