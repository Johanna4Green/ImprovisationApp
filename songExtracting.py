# this class returns an array with tuples of array withchord notes and the notelength 

import mido
from mido import MidiFile
from mido import MetaMessage


class SongExtracting():

    def __init__(self):
        #self.midiFILE = ('AkkordeGDur.mid')
        self.noteArray = []
        self.overallTime = 0
        self.notelength = 'WHOLE'
        self.tuple = []
        self.fileContent = []

        
    def getNotesOfSong(self, midFILE):
        #self.overallTime = 0.10104166666666667  # WholeNote before
        #self.overallTime = 0.051041666666666666 # HalfNote before
        #self.overallTime = 0.026041666666666668 # QuarterNote before
        #self.overallTime = 0.013541666666666667 # EighthNote before
        #self.overallTime = 0.007291666666666667 # SixteenthNote before
        for msg in MidiFile(midFILE):
            if(msg.type != 'program_change' and msg.type != 'control_change') and not msg.is_meta:
                #print(msg)
                # calculate time since start
                self.overallTime = self.overallTime + msg.time

                if(msg.velocity > 0): # noteon
                    self.noteArray.append(msg.note)
                else:  # noteoff
                    if (msg.time != 0):
                        # calculate length of this tone
                        self.notelength = self.determineLength(msg.time)
                        self.tuple.append(self.noteArray)
                        self.tuple.append(self.notelength)
                        self.fileContent.append(self.tuple)
                        self.noteArray =[]
                        self.tuple = []
        print(self.fileContent)
        return self.fileContent   


    def determineLength(self, number):
        div = 1000000   # 1 second has 1 million microseconds
        tempo = 500000  # 1 beat has 500 thousand microseconds
        quarter = tempo/div
        if number > 2*quarter*1.05:             # the number is greater than a half note + 5% => whole note
            self.notelength = 'WHOLE'     
        elif number > quarter*1.05:             # the number is greater than a quarter note + 5% => half note 
            self.notelength = 'HALF'
        elif number > 0.5*quarter*1.05:         # the number is greater than an eighth note + 5% => quarter note
            self.notelength = 'QUARTER'
        elif number > 0.25*quarter*1.05:        # the number is greater than an sixteenth note + 5% => eighth note
            self.notelength = 'EIGHTH'
        elif number > 0.125*quarter*1.05:        # the number is greater than an thirtysecond note + 5% => eighth note
            length = 'SIXTHEENTH'
        else:
            print("ERROR in calculation")
        return self.notelength


    def getTempo(self, midfile):
        for msg in MidiFile(midfile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    #print(msg.tempo)
                    self.tempo = msg.tempo
                    return self.tempo


    def getTonality(self, midfile):
        for msg in MidiFile(midfile):
            if msg.is_meta:
                if msg.type == 'key_signature':
                    #print(msg.tempo)
                    self.tonality = msg.key
                    print(self.tonality)
                    return self.tonality


#se = SongExtracting()
#print(se.getNotesOfSong('AkkordeGDur.mid'))