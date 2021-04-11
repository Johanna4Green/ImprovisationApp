# Akkord-Klasse, die mehrere Noten enthält und auf Basis des "Akkord-Arrays" (notenzeile.py) erstellt wird
# die Notenzeile weiß, wo der Akkord sein soll und sagt es ihm
# und der Akkord weiß dann, wo die Note hin muss

class Chord():

    def __init__(self, chordArray, notelength, tonality, xPosition):
        self.chordArray = chordArray
        self.notelength = notelength
        self.tonality = tonality
        self.xPosition = xPosition

    
    # get chordArray from notenzeile.py
    # containing several notes