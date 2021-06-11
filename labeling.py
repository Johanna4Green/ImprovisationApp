# this class creates all labels: the clef, tact, signs (sharp or flat), the tonality text
# it gets it's information from songExtracting

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QFont

from constants import * 
from songExtracting import SongExtracting


class Labeling():

    song_extracting = SongExtracting()

    def __init__(self):
        self.midifile = MIDIFILE
        self.tonality = self.song_extracting.getTonality(self.midifile)

    #called from gui init
    def init_label(self,window):
        self.window = window
        self.create_clef_label(window)
        self.create_tonality_text_label(window)
        self.create_all_signs(window)
        self.create_tact_label(window)
        self.show_labels()

    #def set_midifile(self, midifile):
    #    self.midifile = midifile
    #    return self.midifile

    # reset function to update from gui when new Backing Track file is choosen
    def reset_labeling_class(self, midifile):
        self.midifile = midifile
        print('in reset labeling')
        print(self.midifile)
        self.tonality = self.song_extracting.getTonality(self.midifile)
        print(self.tonality)
        self.update_labels()

    def reset_tonality_label(self, name):
        self.tonalityLabel.setText(name)

    # update all labels
    def update_labels(self):
        self.tonalityLabel.setText(self.get_tonality_text(self.tonality))
        for i in range(6):
            self.sharp_list[i].setVisible(False)
            self.flat_list[i].setVisible(False)
        self.show_labels()

    # make the according sharp or flat signs visible and move the 4/4 tact sign accordingly
    def show_labels(self):
        tact_C_x_pos = 119
        if self.tonality in SHARP_TONALITIES:
            sharp_num = NUMBERS_OF_SHARPS.get(self.tonality)
            print(sharp_num)
            for i in range(sharp_num):
                self.sharp_list[i].setVisible(True)
            self.tact_x_pos = tact_C_x_pos + sharp_num * 9 
        else:       # self.tonality in FLAT_TONALITY
            flat_num = NUMBERS_OF_FLATS.get(self.tonality)
            print(flat_num)
            for i in range(flat_num):
                self.flat_list[i].setVisible(True)
            self.tact_x_pos = tact_C_x_pos + flat_num * 9
        self.move_tact_label(self.tact_x_pos)
        

    # move tact label according to number of sharp/ flat signs
    def move_tact_label(self, x):
        self.time44Label.move(x, 147)
        self.time44Label.setVisible(True)

    # creating tact label
    def create_tact_label(self, window):
        self.time44Label = QtWidgets.QLabel(window)
        self.time44Label.resize(45,95)
        time44Pixmap = QPixmap('images/timeSign44.png')
        self.time44Label.setPixmap(time44Pixmap)
        self.time44Label.setScaledContents(True)
        self.time44Label.setVisible(False)
        self.time44Label.show()
        # move and show 
        return self.time44Label

    # creating all sharp and flat signs and making them invisible
    def create_all_signs(self,window):
        window = window
        # create list of sharps in order fis cis gis dis ais eis
        self.sharp_list = []
        fis_label = self.create_sharp_label(window, 113, 145)
        self.sharp_list.append(fis_label)
        cis_label = self.create_sharp_label(window, 124, 169)
        self.sharp_list.append(cis_label)
        gis_label = self.create_sharp_label(window, 129, 137)
        self.sharp_list.append(gis_label)
        dis_label = self.create_sharp_label(window, 140, 161)
        self.sharp_list.append(dis_label)
        ais_label = self.create_sharp_label(window, 151, 185)
        self.sharp_list.append(ais_label)
        eis_label = self.create_sharp_label(window, 156, 153)
        self.sharp_list.append(eis_label)
        # create list of flats in order b es as des ges ces
        self.flat_list = []
        b_label = self.create_flat_label(window, 118, 170)
        self.flat_list.append(b_label)
        es_label = self.create_flat_label(window, 126, 146)
        self.flat_list.append(es_label)
        as_label = self.create_flat_label(window, 134, 178)
        self.flat_list.append(as_label)
        des_label = self.create_flat_label(window, 142, 153)
        self.flat_list.append(des_label)
        ges_label = self.create_flat_label(window, 150, 186)
        self.flat_list.append(ges_label)
        ces_label = self.create_flat_label(window, 158, 162)
        self.flat_list.append(ces_label)



    # create one sharp label as template
    def create_sharp_label(self, window, x, y):
        sharpLabel = QtWidgets.QLabel(window)
        sharpLabel.resize(20,30)
        sharpPixmap = QPixmap('images/sharp.png')
        sharpLabel.setPixmap(sharpPixmap)
        sharpLabel.setScaledContents(True)
        sharpLabel.move(x, y)
        sharpLabel.show()
        sharpLabel.setVisible(False)
        return sharpLabel

    # create one flat label as template
    def create_flat_label(self, window, x, y):
        flatLabel = QtWidgets.QLabel(window)
        flatLabel.resize(18,30)
        flatPixmap = QPixmap('images/flat.png')
        flatLabel.setPixmap(flatPixmap)
        flatLabel.setScaledContents(True)
        flatLabel.move(x, y)
        flatLabel.show()
        flatLabel.setVisible(False)
        return flatLabel

  
    # creating the clef label
    def create_clef_label(self,window):
        clefLabel = QtWidgets.QLabel(window)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(65, 132)
        clefLabel.show()

    # creating tonality text label to show tonality to user 
    def create_tonality_text_label(self,window):
        tonalityText = self.get_tonality_text(self.tonality)
        self.tonalityLabel = QtWidgets.QLabel(window)
        self.tonalityLabel.setText(tonalityText)
        #painter.setFont(QFont('Frutiger',20))
        self.tonalityLabel.setFont(QFont("OpenSans-Regular.ttf", 30))     #(QFont('Georgia', 30)) # Skia Helvetica Arial
        self.tonalityLabel.resize(230, 30)
        self.tonalityLabel.move(500,280)
        self.tonalityLabel.show()

    # get the right text for the tonality text label dependent of self.tonality 
    def get_tonality_text(self, ton):
        tonText = ''
        if ton == 'C':
            tonText = 'Tonart: C - Dur'
        elif ton == 'F':
            tonText = 'Tonart: F - Dur'
        elif ton == 'Bb':
            tonText = 'Tonart: B - Dur'
        elif ton == 'Eb':
            tonText = 'Tonart: Es - Dur'
        elif ton == 'Ab':
            tonText = 'Tonart: As - Dur'
        elif ton == 'Db':
            tonText = 'Tonart: Des - Dur'
        elif ton == 'Gb':
            tonText = 'Tonart: Ges - Dur'
        elif ton == 'G':
            tonText = 'Tonart: G - Dur'
        elif ton == 'D':
            tonText = 'Tonart: D - Dur'
        elif ton == 'A':
            tonText = 'Tonart: A - Dur'
        elif ton == 'E':
            tonText = 'Tonart: E - Dur'
        elif ton == 'B':
            tonText = 'Tonart: H - Dur'
        elif ton == 'F#':
            tonText = 'Tonart: Fis - Dur'
        else:
            print('error with tonText in staff line 480')
        return tonText