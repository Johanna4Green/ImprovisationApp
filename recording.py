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

class Recording():

    def __init__(self):
        
        self.fs = self.initFluidSynth()
        self.record_array = []
        self.is_recording = False
        self.playing_recording = False
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
                #print(msg)
                if msg.type == "note_on":
                    self.fs.noteon(msg.channel, msg.note, msg.velocity)
                elif msg.type == "note_off":
                    self.fs.noteoff(msg.channel, msg.note)
                self.last_time = time.time() - self.last_time
                #print(self.last_time)
            print('after record_array is through')
            self.playing_recording = False
            print(self.playing_recording)

    

    def get_playing_recording_state(self):
        return self.playing_recording

    # to save the recording as midi-file in the recording folder 
    def create_midi_file_from_recording(self):  #, record_array):
        print('saving recording')
        delta_time = 0
        mid = MidiFile()
        track = MidiTrack()
        #backing_track= MidiTrack()
        mid.tracks.append(track)
        #mid.tracks.append(backing_track)
        #mid.set_tempo('500000')
        #this_tempo = self.getTempo(mid)
        print(mid.ticks_per_beat)
        print(mid)
        track.append(Message('program_change', program=12, time=0))
        track.append(MetaMessage('set_tempo', tempo=500000))
        for msg in self.record_array:   # append every msg of self.record_array
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


    # to export file
    def export_mid_file(self):
        print('export')
        print('EXPORT DIALOG MUST BE OPENED HERE')
        print('EXPORT BUTTON SHOULD THEN DISAPPEAR')
        #option = QFileDialog.options()
        #file = QFileDialog.getSaveFileName()
        



    def getTempo(self, midifile):
        for msg in MidiFile(midifile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    print(tempo)
                    return tempo

    # to adapt the recording state, when the record button is clicked. 
    def set_record_state(self):
        if self.is_recording == False:
            self.is_recording = True
            self.record_array = []  # if record state is switched on: the record array is cleared from the last input
            self.last_time = time.time()
        else:
            self.is_recording = False  
        print(self.is_recording)
        return self.is_recording

    # to color the recording bubble accordingly (red when recording)
    def draw(self, painter):
        if self.is_recording:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        painter.drawEllipse(775, 290, 10, 10)
        return