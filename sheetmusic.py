# this file creates the sheet music to the given notes.
# it opens MuseScore
from music21 import *
from music21 import note, stream


# https://web.mit.edu/music21/doc/usersGuide/usersGuide_07_chords.html
gMajor = chord.Chord(['G','B','d'])
gMajor.quarterLength = 4

n1 = note.Note('C', quarterLength = 4)
n2 = note.Note('E', quarterLength = 4)
n3 = note.Note('G', quarterLength = 4)
n4 = note.Note('C', quarterLength = 4)


s = stream.Stream()
s.append([gMajor, n1, n2, n3, n4])

s.write('midi', fp = 'ausprobieren.midi')
s.show()

#Theoretisch auch musicxml möglich
#sco = stream.Score()
#s.write('musicxml', fp = 'musicxmlfile.mxl')

#mxlFile = s.write('musicxml', fp = 'musicxmlfile.mxl')
#print(mxlFile)