import mido
import threading
#from thatBTT import FluidSynther
from constants import *

import time
import fluidsynth
from mido import MidiFile




class MidiInput():
    def __init__(self):
        print("in Midi Input thread")
        #self.msg = note_on channel=0 note=94 velocity=55 time=0
        #self.msg = mido.Message #('note_off') #('note_off', note=0, channel=0, velocity=0, time=0)  # (self.type, self.channel, self.note, self.velocity, self.time)
        self.type = 'note_off'
        self.note = 0
        self.velocity = 0
        self.channel = 0 
        #self.nachricht = [self.type, self.note, self.velocity, self.channel]


        #print(self.msg)
        self.keys = [False] * 88 # Key Array kommt hier rein, um Model und View zu trennen = Globale Variable
        input_thread = threading.Thread(target=self.getInput)
        input_thread.start()

    def getKeyArray(self):
        return self.keys

    #def getNachricht(self):
        #nachricht = [self.type, self.note, self.velocity, self.channel]
    #    print("msg got")
    #    print(self.nachricht)
    #    return self.nachricht
       

    def getInput(self):
        #print('in def getInput/ = THREAD')

        inputs = mido.get_input_names() # holt Liste mit allen angeschlossenen Midi-Geräten
        #print(inputs)
        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    print(msg)
                    #print(msg.note)
                    #print(msg.type)
                    #print(msg.channel)
                    #print(msg.velocity)
                    if msg.type =='note_on':
                        self.keys[msg.note] = True  # -36
                    if msg.type == 'note_off':
                        self.keys[msg.note] = False # -36
                    self.type = msg.type
                    self.note = msg.note
                    self.velocity = msg.velocity
                    self.channel = msg.channel
                    #FluidSyntherer.playSound(self.type, self.note, self.velocity, self.channel)
                    self.playSound()
                    #self.playSound(self.type, self.note, self.velocity, self.channel)
                    #print("msg in def Input")
                    #print(self.msg)


    # typei, note, velo, channel)
    def playSound(self):
        print("in playSound")
        #msg = midi_input.getNachricht()    #getMsg()
        print(self.type)
        print(self.note)
        print("after msg")
        #self.typei = typei
        #self.note = note
        #self.velocity = velo
        #self.channel = channel
  
        fs = fluidsynth.Synth(1)
        fs.start(driver = 'portaudio')
    
        sfid = fs.sfload("default-GM.sf2") 
        fs.program_select(0, sfid, 0, 0)
   

        #time.sleep(1.0)
    
        if self.type == "note_on":
            fs.noteon(self.channel, self.note, self.velocity)
            #fs.noteon(0, 67, 30)
            #fs.noteon(0, 76, 30)

            time.sleep(0.2)
        elif self.type == "note_off":
            #fs.noteoff(self.channel, self.note)
            fs.noteoff(0, 67)
            #fs.noteoff(0, 76)
        else:
            print("fail")

            #time.sleep(1.0)
        print("before deleting")
        fs.delete()



#fluidSynther = FluidSynther()
mi = MidiInput()


'''

class FluidSyntherer():

    def ___init___(self, typ, note, velocity, channel):
        self.typ = typ
        self.note = note
        self.velocity = velocity
        self.channel = channel
        #play_thread = threading.Thread(target=self.playSound)
        #play_thread.start()


'''