# creates an information file from the given midi. This is created as a new html file,
# which can be opened in the browser.

import pretty_midi
import pandas as pd
# import IPython.display as ipd

# fn = '/Users/Johanna/PycharmProjects/testToTest/AkkordeGDur.mid'
fn = '/Users/Johanna/PycharmProjects/improvisationApp/AkkordeGDur.mid'

midi_data = pretty_midi.PrettyMIDI(fn)
midi_list = []

for instrument in midi_data.instruments:
    print(midi_data.instruments)
    for note in instrument.notes:
        start = note.start
        end = note.end
        pitch = note.pitch
        #velocity = note.velocity
        midi_list.append([start, end, pitch])   # , velocity, instrument.name

midi_list = sorted(midi_list, key=lambda x: (x[0], x[2]))

print(midi_list)

df = pd.DataFrame(midi_list, columns=['Start', 'End', 'Pitch'])   # , 'Velocity', 'Instrument'
html = df.to_html(index=False)
# ipd.HTML(html)
# print(ipd.HTML(html))

f = open("Anoten.html","w+")
print("f is open")
f.write(html)
f.close()
print("f is closed")
