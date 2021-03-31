# gets the MidiInput from the MidiKeyboard

import mido
import threading
from constants import *

import time
import fluidsynth
from mido import MidiFile

class MidiInput():

    def __init__(self):
        # print("in Midi Input thread")
        self.type = 'note_off'
        self.note = 0
        self.velocity = 0
        self.channel = 0 
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)

        self.keys = [False] * 88 # Key Array kommt hier rein, um Model und View zu trennen = Globale Variable
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
                    #print(msg)
                    if msg.type =='note_on':
                        self.keys[msg.note] = True  # -36
                    if msg.type == 'note_off':
                        self.keys[msg.note] = False # -36
                    self.type = msg.type
                    self.note = msg.note
                    self.velocity = msg.velocity
                    self.channel = msg.channel
                    self.playSound()


    def playSound(self):

        if self.type == "note_on":
            self.fs.noteon(self.channel, self.note, self.velocity)
            #fs.noteon(0, 67, 30)
            #time.sleep(0.2)

        elif self.type == "note_off":
            self.fs.noteoff(self.channel, self.note)
            #self.fs.noteoff(0, 67)

        else:
            print("fail")
        #self.fs.delete()