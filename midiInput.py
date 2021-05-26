# this class containing the input thread processes the midi-keyboard input. 
# it plays the sound with fluidsynth and
# saves the pressed note in an array to be get by the key class and drawn accordingly

import fluidsynth
import mido
from mido import MidiFile
import threading
import time

from constants import *

class MidiInput():

    def __init__(self):
        
        self.fs = self.initFluidSynth()
        self.keys = [False] * 88 # keys array to be gotten from key class and marker drawn accordingly

        input_thread = threading.Thread(target=self.getInput)
        input_thread.start()

    # initializing fluidsynther
    def initFluidSynth(self):
        fs = fluidsynth.Synth(1)
        fs.start(driver = 'portaudio')
        sfid = fs.sfload("sound_midis/default-GM.sf2") 
        fs.program_select(0, sfid, 0, 0)
        return fs

    def getKeyArray(self):
        return self.keys

    # gets input from midi-keyboard and then plays it
    def getInput(self):
        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        #print(inputs)
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    if msg.type =='note_on':
                        self.keys[msg.note + 3] = True  # -36
                    if msg.type == 'note_off':
                        self.keys[msg.note + 3] = False # -36
                    self.play_sound(msg.type, msg.note, msg.velocity, msg.channel)


    # called from getInput: plays midi-keyboard Input live 
    def play_sound(self, note_type, note, velocity, channel):

        if note_type == "note_on":
            self.fs.noteon(channel, note, velocity)

        elif note_type == "note_off":
            self.fs.noteoff(channel, note)

        else:
            print("fail")


# For driver = portaudio to work: brew install portaudio --HEAD 
# https://github.com/gordonklaus/portaudio/issues/41
# head ist entscheidend.
# for fluidsynth: pip install PyFluidSynth 
# version: pyFluidSynth 1.3.0
# Maybe important: PyAudio 0.2.11