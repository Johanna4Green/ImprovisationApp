import mido
import threading 
import time
from mido import MidiFile
import fluidsynth

class BackingTrack():

    btFile = 'sunny.mid'

    def __init__(self):
        # print("in backing track thread")
        self.state = 'paused'  # playing/ paused/ stopped
        # initializing fluidsynther
        self.fs = fluidsynth.Synth(1)
        self.fs.start(driver = 'portaudio')
        self.sfid = self.fs.sfload("default-GM.sf2") 
        self.fs.program_select(0, self.sfid, 0, 0)
        # create thread
        fileInput_thread = threading.Thread(target=self.playFileSound)
        fileInput_thread.start()


    def play_bt(self):
        self.state = "playing"
        return self.state

    def pause_bt(self):
        self.state = "paused"
        return self.state

    def stop_bt(self):
        self.state = "stopped"
        return self.state


    def playFileSound(self):
        while(True): # loop of backing track
            for msg in MidiFile(self.btFile).play():
                if self.state =="playing":
                    print("play is the state")
                    pass
                elif self.state == "paused":
                    while self.state == "paused":
                        print("still paused")
                        time.sleep(0.5)     # as long as bt is paused, waits until play to continue
                        pass
                elif self.state == "stopped":
                    print ("stopped")
                    break
                else:
                    print("Bt failed")
                    break
                if(msg.type != 'program_change' and msg.type != 'control_change'): # nur note-events!
                    # musescore macht irgendwie keine noteoff-Events - ABER die velocity ist 0 wenn die Note aufhört
                    if(msg.velocity > 0): # noteon
                        self.fs.noteon(0, msg.note, msg.velocity)
                    else: # noteoff
                        self.fs.noteoff(0, msg.note)
        self.fs.delete()
