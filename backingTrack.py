import mido
import threading 
import time
from mido import MidiFile
import fluidsynth

class BackingTrack():

    mid = MidiFile('AkkordeGDur.mid')

    def __init__(self):
        #print("in Midi Input thread")
        self.type = 'note_off'
        self.note = 0
        self.velocity = 0
        self.channel = 0
        self.time = 0
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)

        fileInput_thread = threading.Thread(target=self.getFileInput)
        fileInput_thread.start()

   
    def getFileInput(self):

        for i, track in enumerate(self.mid.tracks):
            #print('Track {}: {}'.format(i, track.name))
            if i == 1:
                for msg in track:
                    if not msg.is_meta:
                        print(msg)
                        print(msg.type)
                        print(msg.note)
                        print(msg.time)
                        print(msg.velocity)
                        print(msg.channel)
                        self.type = msg.type
                        self.note = msg.note
                        self.velocity = msg.velocity
                        self.channel = msg.channel
                        self.playFileSound()


    def playFileSound(self):

        time.sleep(0.2)

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

#bt = BackingTrack()