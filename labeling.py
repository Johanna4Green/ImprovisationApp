from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import time
import threading
import mido
from mido import MidiFile
from mido import MetaMessage
import fluidsynth
import math
from constants import * 
from songExtracting import SongExtracting
from chord import Chord


class Labeling():

    song_extracting = SongExtracting()

    def __init__(self):

        self.midFILE = 'sound_midis/AkkordeGDur.mid'
        self.tonality = self.song_extracting.getTonality(self.midFILE)


    def InitLabel(self,window):

        self.create_tonality_Label(window)

        #clef
        clefLabel = QtWidgets.QLabel(window)
        clefLabel.resize(70,125)
        clefPixmap = QPixmap('images/clef.png')
        clefLabel.setPixmap(clefPixmap)
        clefLabel.setScaledContents(True)
        clefLabel.move(65, 132)
        clefLabel.show()
        #takt   
        time44Label = QtWidgets.QLabel(window)
        time44Label.resize(45,95)
        time44Pixmap = QPixmap('images/timeSign44.webp')
        time44Label.setPixmap(time44Pixmap)
        time44Label.setScaledContents(True)
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
    
    def create_tonality_Label(self,window):
        tonalityText = self.getTonalityText(self.tonality)
        tonalityLabel = QtWidgets.QLabel(window)
        tonalityLabel.setText(tonalityText)
        tonalityLabel.setFont(QFont('Arial', 30))
        tonalityLabel.resize(210, 30)
        tonalityLabel.move(510,280)
        tonalityLabel.show()

    def getTonalityText(self, ton):
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