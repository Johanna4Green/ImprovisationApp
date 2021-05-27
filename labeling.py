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

    # reset function to update from gui when new Backing Track file is choosen
    def reset_labeling_class(self, midifile):
        self.midifile = midifile
        print('in reset labeling')
        print(self.midifile)
        self.tonality = self.song_extracting.getTonality(self.midifile)
        print(self.tonality)
        self.update_labels()

    #called from gui init
    def init_label(self,window):
        self.create_clef_label(window)
        self.create_tonality_text_label(window)
        self.create_signs_and_tact_label(window)

    def update_labels(self):
        self.tonalityLabel.setText(self.get_tonality_text(self.tonality))

        """
        # Konstanten
        #number_of_sharps = {'C' : 0, 'G' : 1, ...}
        #number_of_flats = {'A' : 0, '?' : 1, ...}
        self.sharps = number_of_sharps[self.tonality] # int (Anzahl der Kreuze)
        # Äquivalent auf für b?

        # Setze Label Sichtbarkeit
        i = 0
        for label in sharp_labels:
            if i < self.sharps:
                self.sharp_labels[i].set_visible(True)
            else:
                self.sharp_labels[i].set_visible(False)
            i += 1

        # Berechne Einrückung der Taktart
        time_signature_distance = self.sharps * SHARP_LABEL_WIDTH
        time_signature_label.move(XX + time_signature_distance, YY)
        """



    def create_clef_label(self,window):
        clefLabel = QtWidgets.QLabel(window)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(65, 132)
        clefLabel.show()
    
    
    def create_signs_and_tact_label(self,window):
        time44Label = QtWidgets.QLabel(window)
        time44Label.resize(45,95)
        time44Pixmap = QPixmap('images/timeSign44.webp')
        time44Label.setPixmap(time44Pixmap)
        time44Label.setScaledContents(True)

        #sharp_labels = dict()
        #sharp_labels['fis'] = self.create_sharp_label()

        # fisLabel = self.create_sharp_label(100, 50)
        # cisLabel = self.create_sharp_label(120, 60)
        # ...
  
        # leading sign of tonality 
        if self.tonality == 'C':
            time44Label.move(120, 147)
            pass
        # sharp tonalities
        elif self.tonality == 'G': 
            sharLab = self.create_sharp_Label(window)
            sharLab.move(120, 145)
            sharLab.show()
            time44Label.move(150, 147)
        elif self.tonality == 'D':
            for i in range(2):
                sharLab = self.create_sharp_Label(window)
                if i == 0:
                    sharLab.move(116, 145)
                if i == 1:
                    sharLab.move(132, 169)
                sharLab.show() 
                time44Label.move(160, 147)
        elif self.tonality == 'A':
            for i in range(3):
                sharLab = self.create_sharp_Label(window)
                if i == 0:
                    sharLab.move(115, 145)
                if i == 1:
                    sharLab.move(128, 169)
                if i == 2:
                    sharLab.move(141, 137)
                sharLab.show() 
                time44Label.move(160, 147)
        elif self.tonality == 'E':
            for i in range(4):
                sharLab = self.create_sharp_Label(window)
                if i == 0:
                    sharLab.move(115, 145) 
                if i == 1:
                    sharLab.move(127, 169)
                if i == 2:
                    sharLab.move(139, 137)
                if i == 3:
                    sharLab.move(153, 161)
                time44Label.move(165, 147)
                sharLab.show() 
        elif self.tonality == 'B':
            for i in range(5):
                sharLab = self.create_sharp_Label(window)
                if i == 0:
                    sharLab.move(115, 145) 
                if i == 1:
                    sharLab.move(126, 169)
                if i == 2:
                    sharLab.move(137, 137)
                if i == 3:
                    sharLab.move(151, 161)
                if i == 4:
                    sharLab.move(165, 185)
                sharLab.show()
                time44Label.move(174, 147)
        elif self.tonality == 'F#':
            for i in range(7):
                sharLab = self.create_sharp_Label(window)
                if i == 0:
                    sharLab.move(113, 145) 
                if i == 1:
                    sharLab.move(124, 169)
                if i == 2:
                    sharLab.move(129, 137)
                if i == 3:
                    sharLab.move(140, 161)
                if i == 4:
                    sharLab.move(151, 185)
                if i == 5:
                    sharLab.move(156, 153)
                if i == 6:
                    sharLab.move(168, 177)
                time44Label.move(174, 147)
                sharLab.show()
        ### flat tonalities 
        elif self.tonality == 'F':
            flatLab = self.create_flat_Label(window)
            flatLab.move(120, 170)
            flatLab.show()
            time44Label.move(150, 147)
        elif self.tonality == 'Bb':
            for i in range(2):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(120, 170)
                if i == 1:
                    flatLab.move(130, 146)
                flatLab.show()
            time44Label.move(150, 147)
        elif self.tonality == 'Eb':
            for i in range(3):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(120, 170)
                if i == 1:
                    flatLab.move(130, 146)
                if i == 2:
                    flatLab.move(140, 178)
                flatLab.show()
            time44Label.move(160, 147)
        elif self.tonality == 'Ab':
            for i in range(4):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(120, 170)
                if i == 1:
                    flatLab.move(130, 146)
                if i == 2:
                    flatLab.move(140, 178)
                if i == 3:
                    flatLab.move(150, 153)
                flatLab.show()
            time44Label.move(165, 147)
        elif self.tonality == 'Db':
            for i in range(5):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(120, 170)
                if i == 1:
                    flatLab.move(130, 146)
                if i == 2:
                    flatLab.move(140, 178)
                if i == 3:
                    flatLab.move(150, 153)
                if i == 4:
                    flatLab.move(160, 186)
                flatLab.show()
            time44Label.move(170, 147)
        elif self.tonality == 'Gb':
            for i in range(6):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(118, 170)
                if i == 1:
                    flatLab.move(127, 146)
                if i == 2:
                    flatLab.move(136, 178)
                if i == 3:
                    flatLab.move(145, 153)
                if i == 4:
                    flatLab.move(154, 186)
                if i == 5:
                    flatLab.move(163, 162)
                flatLab.show()
            time44Label.move(175, 147)
        elif self.tonality == 'Cb':
            for i in range(7):
                flatLab = self.create_flat_Label(window)
                if i == 0:
                    flatLab.move(118, 170)
                if i == 1:
                    flatLab.move(126, 146)
                if i == 2:
                    flatLab.move(134, 178)
                if i == 3:
                    flatLab.move(142, 153)
                if i == 4:
                    flatLab.move(150, 186)
                if i == 5:
                    flatLab.move(158, 162)
                if i == 6:
                    flatLab.move(166, 194)
                flatLab.show()
            time44Label.move(175, 147)
        else:
            print('do not know this tonality')
            pass  
        time44Label.show()

    def create_sharp_Label(self, window):
        sharpLabel = QtWidgets.QLabel(window)
        sharpLabel.resize(20,30)
        sharpPixmap = QPixmap('images/sharp.png')
        sharpLabel.setPixmap(sharpPixmap)
        sharpLabel.setScaledContents(True)
        return sharpLabel

    def create_flat_Label(self, window):
        flatLabel = QtWidgets.QLabel(window)
        flatLabel.resize(18,30)
        flatPixmap = QPixmap('images/flat.png')
        flatLabel.setPixmap(flatPixmap)
        flatLabel.setScaledContents(True)
        return flatLabel
    
    def create_tonality_text_label(self,window):
        tonalityText = self.get_tonality_text(self.tonality)
        self.tonalityLabel = QtWidgets.QLabel(window)
        #self.tonalityLabel.setStyleSheet("background-color: lightgreen")
        self.tonalityLabel.setText(tonalityText)
        self.tonalityLabel.setFont(QFont('Arial', 30))
        self.tonalityLabel.resize(210, 30)
        self.tonalityLabel.move(510,280)
        self.tonalityLabel.show()

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