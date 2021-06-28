import fluidsynth
import sys

def initFluidSynth():
    fs = fluidsynth.Synth(1)
    platform = sys.platform
    print(platform)
    # https://www.fluidsynth.org/api/CreatingAudioDriver.html
    if 'linux' in platform:
        this_driver = 'alsa'
    elif 'darwin' in platform:
        this_driver = 'portaudio'
    elif 'freebsd' in platform:
        this_driver = 'oss'
    else:
        # windows
        this_driver = 'dsound'
    print(this_driver)
    fs.start(driver = this_driver)
    sfid = fs.sfload("default-GM.sf2") 
    fs.program_select(0, sfid, 0, 0)
    return fs


fs = initFluidSynth()


# For driver = portaudio to work: brew install portaudio --HEAD 
# https://github.com/gordonklaus/portaudio/issues/41
# head ist entscheidend.
# for fluidsynth: pip install PyFluidSynth 
# version: pyFluidSynth 1.3.0
# Maybe important: PyAudio 0.2.11