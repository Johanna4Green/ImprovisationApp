# this class containing the record thread records the midi-keyboard input. 
# it plays the sound with fluidsynth

from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt  

import fluidsynth
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
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
                        msg.time = time.time() - self.last_time
                        self.last_time = time.time()
                    else:
                        pass

    def start_listening_to_recording_thread(self):
        listen_to_recording_thread = threading.Thread(target=self.listen_to_recording)
        listen_to_recording_thread.start()

    def listen_to_recording(self):
        
        #print(self.record_array)
        for msg in self.record_array:
            time.sleep(msg.time)
            #print(msg)
            if msg.type == "note_on":
                self.fs.noteon(msg.channel, msg.note, msg.velocity)
            elif msg.type == "note_off":
                self.fs.noteoff(msg.channel, msg.note)
            self.last_time = time.time() - self.last_time
            #print(self.last_time)


    def create_midi_file_from_recording(self):  #, record_array):
        print('saving recording')
        delta_time = 0
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        #mid.set_tempo('500000')
        #this_tempo = self.getTempo(mid)
        print(mid.ticks_per_beat)
        print(mid)
        track.append(Message('program_change', program=12, time=0))
        track.append(MetaMessage('set_tempo', tempo=500000))
        for msg in self.record_array:
            print(msg.time)
            delta_time = int(mido.second2tick(msg.time, mid.ticks_per_beat, 500000))
            #scale = 500000 * 1e-6 / 480
            #t = msg.time / scale
            #print(t)
            msg.time = delta_time
            print(msg.time)
            print(msg)
            track.append(msg)

        mid.save('recordings/recording.mid')
    # https://sourcecodequery.com/example-method/mido.second2tick



    def getTempo(self, midifile):
        for msg in MidiFile(midifile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    print(tempo)
                    return tempo

    def set_record_state(self):
        if self.is_recording == False:
            self.is_recording = True
            self.last_time = time.time()
        else:
            self.is_recording = False
            
        print(self.is_recording)
        return self.is_recording

    def draw(self, painter):
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(775, 290, 10, 10)
        return