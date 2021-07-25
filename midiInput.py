# this class containing the input thread processes the midi-keyboard input. 
# it plays the sound with fluidsynth and
# saves the pressed note in an array to be get by the key class and drawn accordingly

import fluidsynth
import mido
from mido import MidiFile
import threading
import time

from fluidsynther import fs # fluidsynther for making the sound
from constants import *

class MidiInput():

    def __init__(self):
        self.keys = [False] * 88 # keys array to be gotten from key class and marker drawn accordingly
        
        
    def start(self, device):
        self.device = device 
        self.input_thread = threading.Thread(target=self.getInput)  
        self.input_thread.start()
       


    def getKeyArray(self):
        return self.keys

    # gets input from midi-keyboard and then plays it
    def getInput(self):
        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        #print(inputs)
        with mido.open_input(self.device) as p:
        #with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    if msg.type =='note_on':
                        self.keys[msg.note + 3] = True
                    if msg.type == 'note_off':
                        self.keys[msg.note + 3] = False
                    self.play_sound(msg.type, msg.note, msg.velocity, msg.channel)


    # called from getInput: plays midi-keyboard Input live 
    def play_sound(self, note_type, note, velocity, channel):

        if note_type == "note_on":
            fs.noteon(channel, note, velocity)

        elif note_type == "note_off":
            fs.noteoff(channel, note)

        else:
            print("fail")