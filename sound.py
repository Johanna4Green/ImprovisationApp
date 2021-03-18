# This file plays the audio of the given midi.
# Because of the -1 in pygame.mixer.music.play(-1) it is looped

# 2nd answer: https://stackoverflow.com/questions/6030087/play-midi-files-in-python

# from pretty_midi import PrettyMIDI
# from IPython.display import Audio
import pygame
import keyboard

def play_music(midi_filename):
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play(-1)     # put -1 for looping
    while pygame.mixer.music.get_busy():
        clock.tick(30)      # check if playback has finished

midi_filename = 'Alone.mid'

# mixer config
freq = 44100  # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024   # number of samples

pygame.mixer.init(freq, bitsize, channels, buffer)

try:
    play_music(midi_filename)
except KeyboardInterrupt:

    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit