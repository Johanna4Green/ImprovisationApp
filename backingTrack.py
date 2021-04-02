import mido
import threading 
import time
from mido import MidiFile
import fluidsynth

class BackingTrack():

    mid = MidiFile('AkkordeGDur.mid')

    def __init__(self):
        print("in backing track thread")
        self.state = 'paused'  # playing/ paused/ stopped
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


    def play_bt(self):
        print("in play_bt")
        self.state = "playing"
        return self.state
        #self.getFileInput()

    def pause_bt(self):
        print("in pause_bt")
        self.state = "paused"
        return self.state
        #self.getFileInput()

    def stop_bt(self):
        print("in stop_bt")
        self.state = "stopped"
        return self.state
        #self.getFileInput()

   
    def getFileInput(self):
        print("in getFIleInput")
        for i, track in enumerate(self.mid.tracks):
            print("in getFileInput for loop")
            #print('Track {}: {}'.format(i, track.name))
            if i == 1:
                for msg in track:
                    if self.state =="playing":
                        print("play is the state")
                        pass
                    elif self.state == "paused":
                        while self.state == "paused":
                            print("still paused")
                            time.sleep(0.5)
                            pass
                    elif self.state == "stopped":
                        print ("stopped")
                        break
                    else:
                        print("Bt failed")
                        break
                    if not msg.is_meta:
                        print(msg)
                        print(msg.time)
                        print(msg.velocity)
                        self.type = msg.type
                        self.note = msg.note
                        self.velocity = msg.velocity
                        self.channel = msg.channel
                        self.time = msg.time
                        #for sameStart in msg:
                        #    if msg.time  -> check if 0 or other,
                        # if msg.time == "0":
                        #       append msg to an array,
                        # if msg.time != "0":
                        #       self.playFileSound(array)
                        #       array.clear
                        #       append msg to emptied array
                        self.playFileSound()


    def playFileSound(self): #array

        #time.sleep(0.2)
        # x = 0
        # for msg in array[x]:
        if self.type == "note_on":
            self.fs.noteon(self.channel, self.note, self.velocity)
            #fs.noteon(0, 67, 30)

            #time.sleep(0.2)
        elif self.type == "note_off":
            self.fs.noteoff(self.channel, self.note)
            #self.fs.noteoff(0, 67)
        else:
            print("fail")
        #x+1

#bt = BackingTrack()        