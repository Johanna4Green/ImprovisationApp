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
from constants import * 
from songExtracting import SongExtracting
from chord import Chord

class Staff():

    song_extracting = SongExtracting()

    # TODO: Midi-File auslagern
    def __init__(self):

        self.state = 'stopped'
        # initializing fluidsynther
        self.fs = self.initFluidSynth()

        self.midifile = MIDIFILE
        self.song_chords = self.song_extracting.getNotesOfSong(self.midifile)
        self.tonality = self.song_extracting.getTonality(self.midifile)
        self.length_of_array = len(self.song_chords)
        
        self.x1_hor = NOTELINE_HOR_X1
        self.x2_hor = NOTELINE_HOR_X2
        self.y1_ver = NOTELINE_VER_Y1
        self.y2_ver = NOTELINE_VER_Y2
        self.x_position = self.set_x_position() # NOTELINE_VER_X
        self.basic_x_pos_list = []  # list of all x_positions to return to start position, when e.g. stop is pressed
        self.chord_list = self.get_chords(self.song_chords)
        #self.chordListOfBeginning = self.get_chords(self.song_chords)
        self.bt_keys = [False] * 88 # Key Array in init, um Model und View zu trennen = Globale Variable
        fileInput_thread = threading.Thread(target=self.play_track)
        fileInput_thread.start()

    #def set_midifile(self, midifile):
    #    self.midifile = midifile
    #    return self.midifile

    # initializing fluidsynther
    def initFluidSynth(self):
        fs = fluidsynth.Synth(1)
        fs.start(driver = 'portaudio')
        sfid = fs.sfload("sound_midis/default-GM.sf2") 
        fs.program_select(0, sfid, 0, 0)
        return fs


    ################# RESET ######################
    def reset_staff_class(self, midifile):
        self.state = "stopped"
        self.midifile = midifile
        self.basic_x_pos_list = []

        self.song_chords = self.song_extracting.getNotesOfSong(self.midifile)
        self.tonality = self.song_extracting.getTonality(self.midifile)
        self.length_of_array = len(self.song_chords)
        self.x_position = self.set_x_position() # NOTELINE_VER_X
        print(self.song_chords)
        print(self.length_of_array)
        
        self.chord_list = self.get_chords(self.song_chords)
        #self.state = "stopped"
        
    ############################################

    def get_bt_key_array(self):
        return self.bt_keys

    def reset_chords(self):
        i = 0
        for chord in self.chord_list: 
            chord.reset_x_position(self.basic_x_pos_list[i]) # when stop is clicked: reset x-position
            i = i + 1

    # method to play the backing track, in init as thread to be played simultaneously to input, recording, etc.
    def play_track(self):
        sum_up_len = 0 # to calculate overall_length (sum of all notelength added note by note)
        counter = 0
        while True:
            sum_up_len = 0
            counter = 0
            while self.state == "stopped":
                time.sleep(0.1)
            for entry in self.song_chords:  # entry[0] = note_array / entry[1] = note_length
                counter = counter % self.length_of_array 
                if self.state =="playing":
                    pass
                elif self.state == "paused":
                    while self.state == "paused":
                        time.sleep(0.5)     # as long as bt is paused, waits until play to continue
                        pass
                elif self.state == "stopped":
                    self.reset_chords()
                    break
                else:
                    print("Bt failed")
                    break
                length = self.get_time_of_length(entry[1]) # notelength of current chord
                sum_up_len = sum_up_len + length # adding latest notelength to sum_up_length
                for note in entry[0]:
                    self.bt_keys[note + 3] = True   # draw dot on key
                    self.fs.noteon(0, note, 60)     # play note
                time.sleep(length-0.1)              # sleep the notelength to hold it the notlength (-0.1 to use the 0.1 for the noteoff event in order to hear a short break between notes)
                for note in entry[0]:
                    self.bt_keys[note + 3] = False  
                    self.fs.noteoff(0, note)
                time.sleep(0.1)
                # to move when tact is over: 
                # cannot work because the chord is moved to the pos of the last chord, but this can only work if all chords have equal length! 
                # FIX NEEDED
                if sum_up_len % 2 == 0:    # >= 2
                    last_chord_pos = self.chord_list[counter - 1].get_x_position() # hol die x-Position vom letzten Akkord
                    for chord in self.chord_list:
                        chord.update_x_position()
                        self.chord_list[counter].set_x_position(last_chord_pos)    # looping     #.x_position = last_chord_pos # setz den gerade "rausgeschobenen nach ganz hinten  
                counter = counter + 1 
        self.fs.delete()
    

    # draws the noteline AND calls the chord.draw function to draw the notes onto the noteline
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
        for chord in self.chord_list:
            x = chord.get_x_position()
            if x < 210 or x > (1120 - NOTEWIDTH):
                pass
            else:
                chord.draw(painter)     # draws notes through draw of chord and singlenote!


    # to handle the x-positioning of the chords: get x_pos according to notelength and 
    def get_chords(self, song_chords):
        list_of_chords = []
        self.basic_x_pos_list.append(210)
        for entry in song_chords:
            list_of_chords.append(Chord(entry[0], entry[1], self.tonality, self.x_position))
            self.x_position = self.x_position + self.get_x_distance_of_length(entry[1]) # get x distance to prior chord by notelength       # X_DISTANCE/2  #224  X_DISTANCE/4 für viertel 
            self.basic_x_pos_list.append(self.x_position)  # to save first/ reset position 
        return list_of_chords


    # get x-distance to prior chord by notelength
    def get_x_distance_of_length(self,length):
        x_distance = 0
        if length == 'WHOLE':
            x_distance = X_DISTANCE
        elif length == 'HALF':
            x_distance = X_DISTANCE/2
        elif length == 'QUARTER':
            x_distance = X_DISTANCE/4
        else:
            x_distance = X_DISTANCE/8
        return x_distance

    # get playtime/ length of note to play by notelength
    def get_time_of_length(self, length):
        time = 0
        if length == 'WHOLE':
            time = 2.0
        elif length == 'HALF':
            time = 1.0
        elif length == 'QUARTER':
            time = 0.5
        else:
            time = 0.25
        return time


    def set_x_position(self):
        xPos = 210 #NOTELINE_VER_X
        return xPos



    # change state when button pressed  
    def play_bt(self):
        self.state = "playing"
        return self.state

    # change state when button pressed
    def pause_bt(self):
        self.state = "paused"
        return self.state

    # change state when button pressed
    def stop_bt(self):
        self.state = "stopped"
        return self.state
