# this class containing the record thread records the midi-keyboard input. 
# it plays the sound with fluidsynth

from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import QFileDialog

import fluidsynth
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import threading
import time
from constants import *
from fluidsynther import fs # fluidsynther for making the sound

class Recording():

    def __init__(self):
        
        self.record_array = []
        self.is_recording = False
        self.playing_recording = False
        self.last_time = 0.0
        self.midifile = MIDIFILE
        self.tempo_var = 500000
        record_thread = threading.Thread(target=self.record_input)
        record_thread.start()

    def reset(self, midifile):
        self.midifile = midifile
    
    def change_tempo(self, bpm):
        midi_tempo = (60/ bpm) * 1000000
        self.tempo_var = int(midi_tempo)


    # recording the midi-input and appending all messages to the record_array
    def record_input(self):
        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    if self.is_recording:
                        self.record_array.append(msg)
                        msg.time = time.time() - self.last_time
                        self.last_time = time.time()    # getting the time, as it is not in the midi-input
                    else:
                        pass



    def start_listening_to_recording_thread(self):
        listen_to_recording_thread = threading.Thread(target=self.listen_to_recording)
        listen_to_recording_thread.start()

    # when the listen to recording button of gui is clicked: the latest recording is played
    def listen_to_recording(self):
        if self.record_array == []:
            print('Nothing to play here you need to record something first')
        else:
            self.playing_recording = True
            for msg in self.record_array:
                time.sleep(msg.time)    # wait the time to play each note at its time
                if msg.type == "note_on":
                    fs.noteon(msg.channel, msg.note, msg.velocity)
                elif msg.type == "note_off":
                    fs.noteoff(msg.channel, msg.note)
                self.last_time = time.time() - self.last_time
            self.playing_recording = False


    def get_playing_recording_state(self):
        return self.playing_recording

    # to save the recording as midi-file in the recording folder 
    def create_midi_file_from_recording(self):
        print('saving recording')
        delta_time = 0
        mid = MidiFile()
        mid.type = 1
        track = MidiTrack()
        backing_track= MidiTrack()
        mid.tracks.append(track)
        mid.tracks.append(backing_track)
        
        track_time = 0
        track.append(Message('program_change', program=12, time=0))
        track.append(MetaMessage('set_tempo', tempo=self.tempo_var))
        for msg in self.record_array:   # append every msg of self.record_array
            delta_time = int(mido.second2tick(msg.time, mid.ticks_per_beat, self.tempo_var))
            msg.note = msg.note + 12
            track_time = track_time + msg.time
            msg.time = delta_time
            track.append(msg)

        backing_track.append(Message('program_change', program=12, time=0))
        backing_track.append(MetaMessage('set_tempo', tempo=self.tempo_var))

        backing_track_time = 0 
        while backing_track_time < track_time:
            loop = True
            for bmsg in MidiFile(self.midifile):
                if(bmsg.type != 'program_change' and bmsg.type != 'control_change') and not bmsg.is_meta:
                    bmsg.note = bmsg.note - 24 # -24 to move the note 2 oktaves down to be shown in bass clef
                    bdelta_time = int(mido.second2tick(bmsg.time, mid.ticks_per_beat, self.tempo_var))
                    backing_track_time = backing_track_time + bmsg.time

                    bmsg.time = bdelta_time
                    if loop == True: 
                        bmsg.time = 97
                        loop = False
                    backing_track.append(bmsg)
        loop = True
        return mid
    # https://sourcecodequery.com/example-method/mido.second2tick


    def getTempo(self, midifile):
        for msg in MidiFile(midifile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    return tempo

    # to adapt the recording state, when the record button is clicked. 
    def set_record_state(self):
        if self.is_recording == False:
            self.is_recording = True
            self.record_array = []  # if record state is switched on: the record array is cleared from the last input
            self.last_time = time.time()
        else:
            self.is_recording = False
        return self.is_recording

    # to color the recording bubble accordingly (red when recording)
    def draw(self, painter):
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(745, 290, 10, 10)
        return