# this file gets input from the USB-cable-connected Midi-Keyboard and
# return On-/ Off- Events in Console
# To hear sound you have to open reaper and put the midi-input on a track with a chosen instrument
# python-rtmidi must be installed to get this work

import pygame
import pygame.midi
import time
import mido
import threading

class Midoinput():

    def __init__(self):
        self.get_Input_thread = threading.Thread(target=self.getInput)
        self.get_Input_thread.start()
        

    #def __init__(self, notennumber):
    #    self.notenumber = notenumber
    keyArray = []
    for i in range(88):
        #print(i)
        keyArray.append(False)
    #print(keyArray)

    def getInput(self):
        keyArray = []
        keyArray = Midoinput.keyArray
        inputs = mido.get_input_names() # hol dir eine Liste mit allen Midi-Geräten, die angeschlossen sind
        print(inputs)

        with mido.open_input(inputs[0]) as p: # hier die [0] mit dem richtigen Gerät ersetzen
            for msg in p:
                print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    print(msg.note)
                    print(msg.type)
                    if msg.type =='note_on':
                        print("note ON is the type")
                        keyArray[msg.note - 36] = True
                        print(keyArray)
                    if msg.type == 'note_off':
                        print("note OFF is the type")
                        keyArray[msg.note - 36] = False
                        print(keyArray)



testo = Midoinput()





'''
    def makeNumberToNote(self, notenumber):
        self.notenumber = notenumber
        if notenumber == 36:
            note = 'f'
            print('note is ' + note)
            #drawDot_F
            print("dot is meant to have been drawn")
            #klaviatur.dot_F.draw(klaviatur.canvas)

'''