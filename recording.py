# this class containing the record thread records the midi-keyboard input. 
# it plays the sound with fluidsynth

from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt  

import fluidsynth
import mido
from mido import MidiFile
import threading
import time
from constants import *

class Recording():

    def __init__(self):
        
        self.fs = self.initFluidSynth()
        self.record_array = []
        self.is_recording = False

        record_thread = threading.Thread(target=self.record_input)
        record_thread.start()

    # initializing fluidsynther
    def initFluidSynth(self):
        fs = fluidsynth.Synth(1)
        fs.start(driver = 'portaudio')
        sfid = fs.sfload("sound_midis/default-GM.sf2") 
        fs.program_select(0, sfid, 0, 0)
        return fs



    def record_input(self):
        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    if self.is_recording:
                        self.record_array.append(msg)
                        print(msg)
                    else:
                        pass
                   
   


    def listen_to_recording(self):
        print('listen to recording')
        print(self.record_array)
        for msg in self.record_array:
            time.sleep(msg.velocity/100)
            print(msg)
            if msg.type == "note_on":
                self.fs.noteon(msg.channel, msg.note, msg.velocity)
            elif msg.type == "note_off":
                self.fs.noteoff(msg.channel, msg.note)


    def set_record_state(self):
        if self.is_recording == False:
            self.is_recording = True
        else:
            self.is_recording = False
        print(self.is_recording)
        return self.is_recording

    def draw(self, painter):
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(895, 290, 10, 10)
        return