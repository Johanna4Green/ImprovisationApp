# In this file the music21 plugin "somehow" calculates the tonality and
# returns it in the terminal.

import music21

score = music21.converter.parse('Alone.mid')

key = score.analyze('key')
key1 = score.analyze('Krumhansl')
key2 = score.analyze('AardenEssen')

print(key1.tonic.name, key1.mode)