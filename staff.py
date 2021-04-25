# die Notenzeile zeichnet Linien, Notenschlüssel etc und hat Instanzen der Noten-Klasse
# Notenzeile, die sich um das "drumherum" wie Linien und Notenschlüssel kümmert 
# UND mehrere Akkorde enthält, die dann gezeichnet werden
# die Notenzeile weiß, wo der Akkord sein soll und sagt es ihm (und der Akkord weiß dann, wo die Note hin muss)
# "Hauptklasse" des Programms (GUI) erstellt eine neue Instanz der Notenzeile

# <meta message time_signature>
# numerator=4 denominator=4 means 4/4 Takt
# clocks_per_click=24 means that the metronome will click once every 24 MIDI clocks. 
# notated_32nd_notes_per_beat=8 means that there are eight 32nd notes per beat.


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

class Staff():

    song_extracting = SongExtracting()

    def __init__(self):

        self.state = 'paused'  # playing/ paused/ stopped
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("sound_midis/default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)

        self.midFILE = 'sound_midis/AkkordeGDur.mid'
        self.songChords = self.song_extracting.getNotesOfSong(self.midFILE)
        self.tonality = self.song_extracting.getTonality(self.midFILE)
        self.lengthOfArray = len(self.songChords)
        print(self.lengthOfArray)
        self.xPosition = self.setXPosition()#NOTELINE_VER_X

        self.basicXPosList = []
        self.x1_hor = NOTELINE_HOR_X1
        self.x2_hor = NOTELINE_HOR_X2
        self.y1_ver = NOTELINE_VER_Y1
        self.y2_ver = NOTELINE_VER_Y2
        self.chordList = self.getChords(self.songChords)
        self.chordListOfBeginning = self.getChords(self.songChords)
        
        print('basicXPosList', self.basicXPosList)
        fileInput_thread = threading.Thread(target=self.playTrack)
        fileInput_thread.start()


    def playTrack(self):
        listOfChords = []
        len = 0
        counter = 0
        print('in playTrack')
        print(self.lengthOfArray)
        #array[counter % anzahl_akkorde] 
        while True:
            # array[counter % anzahl_akkorde]
            
            #print(count_mod_len)
            for entry in self.songChords:
                counter = counter % self.lengthOfArray
                #print('counter', counter)
                #print('cml', count_mod_len)
                if self.state =="playing":
                    pass
                elif self.state == "paused":
                    while self.state == "paused":
                        time.sleep(0.5)     # as long as bt is paused, waits until play to continue
                        pass
                elif self.state == "stopped":
                    #counter = 0
                    #self.chordList = []
                    #self.chordList = self.getChords(self.songChords)
                    i = 0
                    for chord in self.chordList: 
                        print(chord.chordArray)
                        chord.reset_x_position(self.basicXPosList[i])
                        print(self.basicXPosList[i])
                        i = i + 1
                    #self.fs.delete()
                    #pass
                    break
                else:
                    print("Bt failed")
                    break
                #print('entry1', entry[1])
                #len = entry[1]
                length = self.getTimeOfLength(entry[1])
                len = len + length 
                #print('len', len)
                for entrada in entry[0]:
                    #print(entrada)
                    self.fs.noteon(0, entrada, 60)
                time.sleep(length-0.1)
                for entrada in entry[0]:
                    self.fs.noteoff(0, entrada)
                    #self.xPosition = self.xPosition - X_DISTANCE
                time.sleep(0.1)
                if len % 2 == 0:    # >= 2
                    #print('dividebale by 2')
                    #array[counter % anzahl_akkorde]
                    last_chord_pos = self.chordList[counter - 1].get_x_position() # hol die x-Position vom letzten Akkord
                    print(last_chord_pos)
                    for chord in self.chordList: 
                        #print('chord in listchord', len)
                        #print(chord.xPosition)
                        #self.chordList.append(chord)
                        #self.chordList[count_mod_len].update_x_position()
                        #print(self.chordList)
                        print(chord.chordArray)
                        chord.update_x_position()
                        self.chordList[counter].set_x_position(last_chord_pos)         #.xPosition = last_chord_pos # setz den gerade "rausgeschobenen nach ganz hinten  
                        #print('self.xPos', self.chordList[counter].xPosition)
                        #print('real self.xPosiition', self.xPosition)
                    
                counter = counter + 1 
                #print(counter) 
            #self.chordList.append(chord)
        self.fs.delete()

    def reset_x_position(self):
        self.chordList = self.chordListOfBeginning
        #count = 0
        #for chord in self.chordList: 
        #    chord.xPosition = self.basicXPosList[count]      #self.setXPosition() + (X_DISTANCE * count)
       #     count = count + 1

    #counter = 0
    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # set pen to draw the outline of the key
        # horizontal lines / staves
        y = NOTELINE_HOR_Y
        for line in range(5):
            painter.drawLine(self.x1_hor, y, self.x2_hor, y)
            y = y + Y_DISTANCE
        # vertical lines / bar line
        x = NOTELINE_VER_X
        for line in range(3):
            painter.drawLine(x, self.y1_ver, x, self.y2_ver)
            x = x + X_DISTANCE
        # draw chords 
        #count_mod_len = self.counter % self.lengthOfArray
        #print('cml', count_mod_len)
        for chord in self.chordList:
            
            #self.counter = self.counter +1 
            x = chord.get_x_position()
            #print(type(x))
            #print('x in chord drawing', x)
            if x < 210 or x > (1120 - NOTEWIDTH):
                pass
            else:
                #print('in draw in staff', chord.xPosition)
                chord.draw(painter)  
                #print(self.counter)
        #print(self.counter)




    def getChords(self, songchords):
        listOfChords = []
        #print('in getChords')
        # array[counter % anzahl_akkorde]
        self.basicXPosList.append(210)
        for entry in songchords:
            #print(self.xPosition)
            #print(entry[0], entry[1], self.tonality, self.xPosition)
            listOfChords.append(Chord(entry[0], entry[1], self.tonality, self.xPosition))
            self.xPosition = self.xPosition + self.getXDistanceOfLength(entry[1])       #X_DISTANCE/2  #224  X_DISTANCE/4 für viertel 
            print('line 171', self.xPosition)
            self.basicXPosList.append(self.xPosition)
        return listOfChords



    def getXDistanceOfLength(self,length):
        #print(length)
        xDistance = 0
        if length == 'WHOLE':
            xDistance = X_DISTANCE
        elif length == 'HALF':
            xDistance = X_DISTANCE/2
        elif length == 'QUARTER':
            xDistance = X_DISTANCE/4
        else:
            xDistance = X_DISTANCE/8
        #print(xDistance)
        return xDistance

    
    def getTimeOfLength(self, length):
        #print(length)
        #print(type(length))
        time = 0
        if length == 'WHOLE':
            time = 2.0
        elif length == 'HALF':
            time = 1.0
        elif length == 'QUARTER':
            time = 0.5
        else:
            time = 0.25
        #print(time)
        return time


    def setXPosition(self):
        xPos = 210 #NOTELINE_VER_X
        return xPos
        
    def play_bt(self):
        self.state = "playing"
        return self.state

    def pause_bt(self):
        self.state = "paused"
        return self.state

    def stop_bt(self):
        self.state = "stopped"
        return self.state


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
