import fluidsynth


def initFluidSynth():
    fs = fluidsynth.Synth(1)
    fs.start(driver = 'portaudio')
    sfid = fs.sfload("default-GM.sf2") 
    fs.program_select(0, sfid, 0, 0)
    return fs

fs = initFluidSynth()