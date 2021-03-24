# gets the MidiInput from the MidiKeyboard

import mido
import threading
from constants import *


class MidiInput():
    def __init__(self):
        self.keys = [False] * 88 # Key Array kommt hier rein, um Model und View zu trennen
        input_thread = threading.Thread(target=self.getInput)
        input_thread.start()

    def getKeyArray(self):
        return self.keys

    def getInput(self):
        #print('in def getInput/ = THREAD')

        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        #print(inputs)
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    #print(msg.note)
                    #print(msg.type)
                    if msg.type =='note_on':
                        self.keys[msg.note - 36] = True
                    if msg.type == 'note_off':
                        self.keys[msg.note - 36] = False