import time
import fluidsynth
import mido
from mido import MidiFile
from midiInput import MidiInput
import threading

# For driver = portaudio to work: brew install portaudio --HEAD 
# https://github.com/gordonklaus/portaudio/issues/41
# head ist entscheidend.
# for fluidsynth: pip install PyFluidSynth 
# version: pyFluidSynth 1.3.0
# Maybe important: PyAudio 0.2.11

class FluidSynther():

    def __init__(self):
        #self.type = type    # note_on/ note_off
        #self.note = msg.note
        #self.channel = msg.channel
        #self.velocity = msg.velocity
        print("in FLuidSynther init")
        #print(self.type)
        #print(self.note)
        play_thread = threading.Thread(target=self.playSound)
        play_thread.start()



    def playSound(self):

        msg = midi_input.getNachricht()    #getMsg()
        print(msg)
        typei = msg[0]
        note = msg[1]
        velocity = msg[2]
        channel = msg[3]

        fs = fluidsynth.Synth(1)
        fs.start(driver = 'portaudio')

        sfid = fs.sfload("default-GM.sf2") 
        fs.program_select(0, sfid, 0, 0)


        #time.sleep(1.0)
    
        if typei == "note_on":
            fs.noteon(channel, note, velocity)
            #fs.noteon(0, 67, 30)
            #fs.noteon(0, 76, 30)

            #time.sleep(1.0)
        elif typei == "note_off":
            fs.noteoff(channel, note)
            #fs.noteoff(0, 67)
            #fs.noteoff(0, 76)
        else:
            print("fail")

            #time.sleep(1.0)

        fs.delete()
    
    #def getMessage():

midi_input = MidiInput()
#pl = FluidSynther()
#pl.playSound()


'''
noteon channel key velocity

Send a note-on event
noteoff channel key

Send a note-off event
'''