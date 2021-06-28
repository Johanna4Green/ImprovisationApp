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
SHARP_TONALITIES = ['C', 'G', 'D', 'A', 'E', 'B', 'F#']   # C g d a e h fis
NUMBERS_OF_SHARPS = {'C' : 0, 'G' : 1, 'D' : 2, 'A' : 3, 'E' : 4, 'B' : 5, 'F#' : 6}
NUMBERS_OF_FLATS =  {'A' : 0, 'F' : 1, 'Bb' : 2, 'Eb' : 3, 'Ab' : 4, 'Db' : 5, 'Gb' : 6, 'Cb': 7}



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

MIDIFILE = 'sound_midis/CDur_Example.mid'

TON_DICT = {
    'C': 'Tonart: C - Dur',
    'F': 'Tonart: F - Dur',
    'Bb': 'Tonart: B - Dur',
    'Eb': 'Tonart: Es - Dur',
    'Ab': 'Tonart: As - Dur',
    'Db': 'Tonart: Des - Dur',
    'Gb': 'Tonart: Ges - Dur',
    'G': 'Tonart: G - Dur',
    'D': 'Tonart: D - Dur',
    'A': 'Tonart: A - Dur',
    'E': 'Tonart: E - Dur',
    'B': 'Tonart: H - Dur',
    'F#': 'Tonart: Fis - Dur'
}


#[ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
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
c_dur_penta_notes = [0, 3, 5, 7, 10]
fis_dur_penta_notes = [1, 4, 6, 9, 11]


COLORING_DICT = {
    'C': c_dur_notes,
    'G': g_dur_notes,
    'D': d_dur_notes,
    'A': a_dur_notes,
    'E': e_dur_notes,
    'B': b_dur_notes,
    'F#': fis_dur_notes,
    'F': f_dur_notes,
    'Bb': bb_dur_notes,
    'Eb': es_dur_notes,
    'Ab': as_dur_notes,
    'Db': des_dur_notes,
    'Gb': ges_dur_notes,
    'c-penta': c_dur_penta_notes,
    'fis-penta': fis_dur_penta_notes
        }