import music21 as m21
import matplotlib.pyplot as plt
from matplotlib import image

n = m21.note.Note('c')
#n.write('lily.png', fp='test_note') # benutzt lilypond
n.write('musicxml.png', fp='test_note') # benutzt musescore


# zeig das Bild an - geht natürlich auch mit pygame etc
img = image.imread('test_note-1.png')
plt.show()
#plt.imshow()
#plt.show()
