import jack

import numpy as np
import matplotlib.pyplot as plt
from _tkinter import TclError

from scipy.fft import rfft, rfftfreq

client = jack.Client("FFT_plotter")
in_port = client.inports.register("audio_in")
blocksize = client.blocksize

# These are to play with.
freq_divisor = 32
buff_multiplier = 32

batch_size = blocksize / freq_divisor
signal_length = int(blocksize * buff_multiplier / freq_divisor)
signal = np.ndarray(signal_length)
signal_samplerate = client.samplerate / freq_divisor
print("Signal length:\t\t", signal_length)
print("Signal samplerate:\t", signal_samplerate)

@client.set_process_callback
def process(frames):
    data = in_port.get_array()[::freq_divisor]
    for i in range(buff_multiplier-1):
        signal[int(i*batch_size):int(i*batch_size+batch_size)] = signal[int((i+1)*batch_size):int((i+1)*batch_size+batch_size)]
    signal[int(-1-batch_size):-1] = data

def loop():
    yf = np.abs(rfft(signal[0:-1]))
    xf = rfftfreq(signal_length-1, 1 / signal_samplerate)
    plt.subplot(2, 1, 1)
    plt.clf()
    plt.plot(xf, yf)
    plt.ylim(0, 20)
    plt.pause(0.1)

with client:
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        print(" Program terminated by user. Exiting")
        exit(0)
    except TclError:
        print("Window closed. Exiting")
        exit(0)