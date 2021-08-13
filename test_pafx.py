
import numpy as np
import soundfile as sf

from pafx.comb import Comb
from pafx.allpass import Allpass
from pafx.tapped_delay_line import TappedDelayLine
from pafx.reverb import Reverb, ReverbConfig
from pafx.equalizer import Equalizer
from pafx.echo import Echo
from pafx.chorus import Chorus
from pafx.flanger import Flanger
from pafx.vibrato import Vibrato
from pafx.tremolo import Tremolo

def test_filters(input_file):
    x, fs  = sf.read(input_file)
    comb = Comb(100, 0.9, 0)
    allpass = Allpass(556, 0.5)

    tap_delays = [190,  949,  993,  1183, 1192, 1315,
                    2021, 2140, 2524, 2590, 2625, 2700,
                    3119, 3123, 3202, 3268, 3321, 3515]

    tap_gains = [.841, .504, .49,  .379, .38,  .346,
                    .289, .272, .192, .193, .217,  .181,
                    .18,  .181, .176, .142, .167, .134]

    tdl = TappedDelayLine(tap_delays, tap_gains)  

    yc = np.zeros(len(x))
    ya = np.zeros(len(x))
    yt = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        yc[i] = comb.process(x[i])
        ya[i] = allpass.process(x[i])
        yt[i] = tdl.process(x[i])

    # Save Results
    output_file = "data/comb.wav"
    yc = yc / max(np.abs(yc))
    sf.write(output_file, yc, fs)

    output_file = "data/allpass.wav"
    ya = ya / max(np.abs(ya))
    sf.write(output_file, ya, fs)

    output_file = "data/tpl.wav"
    yt = yt / max(np.abs(yt))
    sf.write(output_file, yt, fs)

def test_eq(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))

    eq_gains = [10, 10, 10, 10, 0, 0, -5, -10, -10, -10]
    eq = Equalizer(eq_gains, fs)
    eq.dump()
    
    # Start Processing
    for i in range(len(x)):
        y[i] = eq.process(x[i])

    output_file = "data/eq.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)
    
def test_reverb(input_file):
    x, fs  = sf.read(input_file)

    config = ReverbConfig()
    config.room_scale = 70
    config.pre_delay = 50
    config.dry_gain = -5
    config.wet_gain = 5
    config.hf_damping = 30
    config.reverberance = 100
    config.stereo_width = 50
    config.er_gain = 0.2
    reverb = Reverb(config, fs)

    y = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        y[i] = reverb.process(x[i])

    output_file = "data/reverb.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)

def test_echo(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))

    echo_gains = [0.5]
    echo_delays = [0.05]
    echo = Echo(fs, echo_delays, echo_gains, 0.5)
    # Start Processing
    for i in range(len(x)):
        y[i] = echo.process(x[i])

    output_file = "data/echo.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)

def test_chorus(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))

    gains = [0.5]
    delays = [0.05]
    mod_widths = [0.005]
    mod_freqs = [2]
    dry_gain = 1
    chorus = Chorus(fs, delays, mod_freqs, mod_widths, gains, dry_gain)
    # Start Processing
    for i in range(len(x)):
        y[i] = chorus.process(x[i])

    output_file = "data/chorus.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)

def test_flanger(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))

    delay = 0.01
    mod_width = 0.003
    mod_freq = 1
    flanger = Flanger(fs, delay, mod_width, mod_freq)
    # Start Processing
    for i in range(len(x)):
        y[i] = flanger.process(x[i])
    output_file = "data/flanger.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)
     
def test_vibrato(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))

    delay = 0.008
    mod_width = 0.004
    mod_freq = 2.3
    vibrato = Vibrato(fs, delay, mod_width, mod_freq)
    # Start Processing
    for i in range(len(x)):
        y[i] = vibrato.process(x[i])
    output_file = "data/vibrato.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)
    
def test_tremolo(input_file):
    x, fs  = sf.read(input_file)
    y = np.zeros(len(x))
    
    mod_depth = 0.5
    mod_freq = 10
    tremolo = Tremolo(mod_freq, mod_depth, fs)
    # Start Processing
    for i in range(len(x)):
        y[i] = tremolo.process(x[i])
    output_file = "data/tremolo.wav"
    y = y / max(np.abs(y))
    sf.write(output_file, y, fs)

def main():

    # Prepare Data 
    input_file = "data/input.wav"
    test_filters(input_file)
    test_eq(input_file)
    test_reverb(input_file)
    test_echo(input_file)
    test_chorus(input_file)
    test_flanger(input_file)
    test_vibrato(input_file)
    test_tremolo(input_file)

if __name__=="__main__":
    main()


