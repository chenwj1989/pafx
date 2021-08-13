import math
'''      
    Low Frequency Oscillator
'''
class LFO():
    def __init__(self, sample_rate, frequency, width, waveform='sine'):
        self.waveform = waveform
        self.width = width
        self.delta = frequency / sample_rate
        self.phase = 0
        return

    def process(self, n):
        return self.width * math.sin(2 * math.pi * self.delta * n)

    def tick(self, i=1):
        ret = self.width * math.sin(2 * math.pi * self.phase)

        self.phase += i * self.delta
        if( self.phase > 1.0):
            self.phase -= 1.0
        return ret
