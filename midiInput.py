# this class containing the input thread processes the midi-keyboard input. 
# it plays the sound with fluidsynth and
# saves the pressed note in an array to be get by the key class and drawn accordingly

from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import fluidsynth
import mido
from mido import MidiFile
import threading
import time

from constants import *

class MidiInput():

    def __init__(self):
        #print("in Midi Input thread")
        self.type = 'note_off'
        self.note = 0
        self.velocity = 0
        self.channel = 0 
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("sound_midis/default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)
        
        self.keys = [False] * 88 # keys array to be gotten from key class and marker drawn accordingly

        self.record_array = []
        self.is_recording = False
        print(self.is_recording)

        input_thread = threading.Thread(target=self.getInput)
        input_thread.start()

    def getKeyArray(self):
        return self.keys

    def getInput(self):
        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        #print(inputs)
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    if self.is_recording:
                        self.record_array.append(msg)
                    else:
                        pass
                    #print(msg)
                    if msg.type =='note_on':
                        self.keys[msg.note + 3] = True  # -36
                    if msg.type == 'note_off':
                        self.keys[msg.note + 3] = False # -36
                    self.type = msg.type
                    self.note = msg.note
                    self.velocity = msg.velocity
                    self.channel = msg.channel
                    self.play_sound()


    def record_input(self):
        if self.is_recording == False:
            self.is_recording = True
        else:
            self.is_recording = False
        print(self.is_recording)
        return self.is_recording

    def listen_to_recording(self):
        print('listen to recording')
        print(self.record_array)
        for msg in self.record_array:
            print(msg)
            if msg.type == "note_on":
                self.fs.noteon(msg.channel, msg.note, msg.velocity)
            #fs.noteon(0, 67, 30)
            #fs.noteon(0, 76, 30)
               
            #time.sleep(1.0)
            elif msg.type == "note_off":
                self.fs.noteoff(msg.channel, msg.note)
            time.sleep(msg.velocity/240)
        #self.fs.delete()
            
            #if msg.type =='note_on':
            #    self.keys[msg.note + 3] = True  # -36
            #if msg.type == 'note_off':
            #    self.keys[msg.note + 3] = False # -36
            #self.type = msg.type
            #self.note = msg.note
            #self.velocity = msg.velocity
            #self.channel = msg.channel
            #self.play_sound()






    def draw(self, painter):
        #painter.setPen(QPen(Qt.black, 1, Qt.SolidLine)) 
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(895, 290, 10, 10)
        return


    def get_record_state(self):
        return self.is_recording

    def play_sound(self):

        if self.type == "note_on":
            self.fs.noteon(self.channel, self.note, self.velocity)

        elif self.type == "note_off":
            self.fs.noteoff(self.channel, self.note)

        else:
            print("fail")

# For driver = portaudio to work: brew install portaudio --HEAD 
# https://github.com/gordonklaus/portaudio/issues/41
# head ist entscheidend.
# for fluidsynth: pip install PyFluidSynth 
# version: pyFluidSynth 1.3.0
# Maybe important: PyAudio 0.2.11