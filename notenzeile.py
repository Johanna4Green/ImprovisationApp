# die Notenzeile zeichnet Linien, Notenschlüssel etc und hat Instanzen der Noten-Klasse
# die Noten-Klasse kümmert sich darum, dass die Note gezeichnet wird

# <meta message time_signature>
# numerator=4 denominator=4 means 4/4 Takt
# clocks_per_click=24 means that the metronome will click once every 24 MIDI clocks. 
# notated_32nd_notes_per_beat=8 means that there are eight 32nd notes per beat.

import mido
from mido import MidiFile
from mido import MetaMessage
import math


class Notenzeile():

    def __init__(self):
        self.midFILE = 'AkkordeGDur.mid'
        self.noteArray = []
        self.overallTime = 0
        self.notelength = 0.5
        self.tempo = 500000

    def getNotesOfSong(self):

        for msg in MidiFile(self.midFILE):
            #print(msg)
            if(msg.type != 'program_change' and msg.type != 'control_change') and not msg.is_meta:
                #print(msg)
                if(msg.velocity > 0): # noteon
                    self.overallTime = self.overallTime + msg.time
                    self.noteArray.append(msg.note)
        
                else:  # noteoff
                    if (msg.time != 0):
                        self.notelength = self.rounding(msg.time)
                        self.overallTime = math.ceil(self.overallTime + msg.time)
                        print(self.noteArray, self.notelength, self.overallTime) #################### THIS IMPORTANT
                        self.noteArray =[]
                    pass


    def rounding(self, number):

        self.div = 1000000
        self.tempo = self.getTempo(self.midFILE)
        if number > (self.tempo/self.div) *2:           # Ganzenote
            number = 2.0     
        #elif number > 1.3 and number < 1.7:            # punktierte Halbe
        #    number = 1.5    
        elif number > self.tempo/self.div:              # Halbenote
            number = 1.0
        elif number > (self.tempo/self.div) /2:         # Viertelnote
            number = 0.5
        elif number > ((self.tempo/self.div) /2) /2:     # Achtelnote
            number = 0.25
        else:
            number = 0
            print("ERROR in calculation")
        return number


    def getTempo(self, midfile):

        for msg in MidiFile(midfile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    #print(msg.tempo)
                    self.tempo = msg.tempo
                    return self.tempo


nz = Notenzeile()
nz.getNotesOfSong()