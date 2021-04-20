
# for drawing the keys correctly: filled in Key.py and used in gui.py
BLACK_KEYS = []
WHITE_KEYS = []
# for appending key to the correct array above, used in key.py
KEY_TYPE_BLACK = 0
KEY_TYPE_WHITE = 1


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





LINES = []
NOTES = []

WINDOW_X = 10
WINDOW_Y = 10
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

DISTANCE_TO_LEFT_MARGIN = 80

# Noteline
NOTELINE_HOR_X1 = 80 #125
NOTELINE_HOR_X2 = 1120#WINDOW_WIDTH - NOTELINE_HOR_X1
NOTELINE_HOR_Y = 160    # 176, 192, 208, 224
Y_DISTANCE = 16
Y_NOTE_DISTANCE = 8


NOTELINE_VER_X = 430#420 #400    # 625, 850, (beginn 125,  1st: 275, 2nd, 3rd, 4th: 225 end: 1075)  --> 50 vor Beginning                # 350, 600, 850                #400, 600, 800
NOTELINE_VER_Y1 = NOTELINE_HOR_Y
NOTELINE_VER_Y2 = NOTELINE_HOR_Y + (4*16)
X_DISTANCE = 230   #224 # 225

NOTEWIDTH = 17
NOTEHEIGHT = 16






'''
# WHITE NOTES
A_NOTES = [1, 13, 25, 37, 49, 61, 73, 85]
B_NOTES = [3, 15, 27, 39, 51, 63, 75, 87]
C_NOTES = [4, 16, 28, 40, 52, 64, 76, 88]
D_NOTES = [6, 18, 30, 42, 54, 66, 78]
E_NOTES = [8, 20, 32, 44, 56, 68, 80]
F_NOTES = [9, 21, 33, 45, 57, 69, 81]
G_NOTES = [11, 23, 35, 47, 59, 71, 83]
# BLACK NOTES
A_MAJ_B_MIN_NOTES = [2, 14, 26, 38, 50, 62, 74, 86]
C_MAJ_D_MIN_NOTES = [5, 17, 29, 41, 53, 65, 77]
D_MAJ_E_MIN_NOTES = [7, 19, 31, 43, 55, 67, 79]
F_MAJ_G_MIN_NOTES = [10, 22, 34, 46, 58, 70, 82]
G_MAJ_A_MIN_NOTES = [12, 24, 36, 48, 60, 72, 84]

# ALL BLACKS
MAJOR_MINOR_NOTES = [2, 14, 26, 38, 50, 62, 74, 86, 5, 17, 29, 41, 53, 65, 77, 7, 19, 31, 43, 55, 67, 79, 10, 22, 34, 46, 58, 70, 82, 12, 24, 36, 48, 60, 72, 84]
'''