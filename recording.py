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
        self.last_time = 0.0
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
                        print(time.time())
                        print(time.time() - self.last_time)
                        this_time = time.time() - self.last_time #self.convert_to_midi_time(time.time() - self.last_time)
                        msg.time = this_time
                        self.last_time = time.time()
                    else:
                        pass
                   
    
    #def convert_to_midi_time(self, number):
        #60000 / (BPM * PPQ)
   #     print(number)
   #     int_ticks = mido.second2tick(number, 3, 500000)
        #print(int_ticks/1000000)
    #    return  int_ticks


    def listen_to_recording(self):
        
        print('listen to recording')
        print(self.record_array)
        for msg in self.record_array:
            #print(time.time())
            #x = time.time()- self.last_time
            #print(x)
            #actual_delta_time = (time.time()-self.last_time) / 10
            time.sleep(msg.time)  #(self.convert_to_midi_time(time.time()-self.last_time))
            #self.last_time = time.time()
            print(msg)
            if msg.type == "note_on":
                self.fs.noteon(msg.channel, msg.note, msg.velocity)
                self.last_time = time.time() - self.last_time
            elif msg.type == "note_off":
                self.fs.noteoff(msg.channel, msg.note)
                self.last_time = time.time() - self.last_time
            print(self.last_time)


    def set_record_state(self):
        start = time.time()
        if self.is_recording == False:
            self.is_recording = True
            self.last_time = time.time()
            #self.start = time.time()
            print(start)
            #print(self.start)
        else:
            end = time.time()
            print(end)
            print(end - start)
            self.is_recording = False
            
        print(self.is_recording)
        return self.is_recording

    def draw(self, painter):
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(895, 290, 10, 10)
        return



'''
du könntest nen Timer starten, wenn record gedrückt wird (vermutlich asynchron als eigener Thread)
dann bei jedem Input-Event die Zeit vom Timer holen
in Midi-Zeit konvertieren (wie das geht steht in der Mido-Doku)
und die time vom Event setzen
'''