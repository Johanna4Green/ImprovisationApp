# this class processes the chosen midifile
# it returns an array with tuples of array with chord notes and the notelength 
# it determines the tonality (and the tempo)

import mido
from mido import MidiFile
from mido import MetaMessage


class SongExtracting():

    def __init__(self):
        self.note_array = []
        self.overall_time = 0
        self.note_length = 'WHOLE'
        self.tuple = []

    # creates array from midi-file with each [[notes of one_chord] length of one_chord]
    def getNotesOfSong(self, midifile):
        self.file_content = []
        #self.overallTime = 0.10104166666666667  # WholeNote before
        #self.overallTime = 0.051041666666666666 # HalfNote before
        #self.overallTime = 0.026041666666666668 # QuarterNote before
        #self.overallTime = 0.013541666666666667 # EighthNote before
        #self.overallTime = 0.007291666666666667 # SixteenthNote before
        for msg in MidiFile(midifile):
            if(msg.type != 'program_change' and msg.type != 'control_change') and not msg.is_meta:
                #print(msg)
                self.overall_time = self.overall_time + msg.time  # calculate time since start
                if(msg.velocity > 0): # noteon
                    self.note_array.append(msg.note - 12)   # -12 to get the sound one octave down
                else:  # noteoff
                    if (msg.time != 0):
                        self.note_length = self.determine_length(msg.time) # calculate length of this tone
                        self.tuple.append(self.note_array)
                        self.tuple.append(self.note_length)
                        self.file_content.append(self.tuple)
                        self.note_array =[]
                        self.tuple = []
        return self.file_content   

    # get the note length 
    def determine_length(self, number):
        div = 1000000   # 1 second has 1 million microseconds
        tempo = 500000  # 1 beat has 500 thousand microseconds
        quarter = tempo/div
        if number > 2*quarter*1.05:             # the number is greater than a half note + 5% => whole note
            self.note_length = 'WHOLE'     
        elif number > quarter*1.05:             # the number is greater than a quarter note + 5% => half note 
            self.note_length = 'HALF'
        elif number > 0.5*quarter*1.05:         # the number is greater than an eighth note + 5% => quarter note
            self.note_length = 'QUARTER'
        elif number > 0.25*quarter*1.05:        # the number is greater than an sixteenth note + 5% => eighth note
            self.note_length = 'EIGHTH'
        elif number > 0.125*quarter*1.05:        # the number is greater than an thirtysecond note + 5% => eighth note
            length = 'SIXTHEENTH'
        else:
            print("ERROR in calculation")
        return self.note_length


    def getTonality(self, midifile):
        for msg in MidiFile(midifile):
            if msg.is_meta:
                if msg.type == 'key_signature':
                    self.tonality = msg.key
                    return self.tonality


    def getTempo(self, midifile):
        for msg in MidiFile(midifile):
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo
                    return self.tempo
