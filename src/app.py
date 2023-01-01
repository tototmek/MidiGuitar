import jack
from datetime import datetime
import signal_processing
import note_detection
import time

import numpy as np
import matplotlib.pyplot as plt
from _tkinter import TclError

from scipy.fft import rfft, rfftfreq

client = jack.Client("MidiGuitar")
in_port = client.inports.register("audio_in")
blocksize = client.blocksize

# These are to play with.
freq_divisor = 8
buff_multiplier = 8

pitch_buffer = np.array([0 for _ in range(100)])

batch_size = blocksize / freq_divisor
signal_length = int(blocksize * buff_multiplier / freq_divisor)
signal = np.ndarray(signal_length)
signal_samplerate = client.samplerate / freq_divisor
print("Signal length:\t\t", signal_length)
print("Signal samplerate:\t", signal_samplerate)
print("Latency:\t\t%.2f" % (1000 * signal_length / signal_samplerate), "ms")


@client.set_process_callback
def process(frames):
    data = in_port.get_array()[::freq_divisor]
    for i in range(buff_multiplier-1):
        signal[int(i*batch_size):int(i*batch_size+batch_size)] = signal[int((i+1)*batch_size):int((i+1)*batch_size+batch_size)]
    signal[int(-1-batch_size):-1] = data

def loop():
    global pitch_buffer
    plt.clf()
    pitch = note_detection.detect_pitch(signal, signal_samplerate, (20, 2000))
    print(pitch)
    pitch_buffer = np.roll(pitch_buffer, -1)
    pitch_buffer[-1] = pitch
    plt.plot(pitch_buffer)
    plt.pause(0.1)

with client:
    try:
        in_port.connect("system:capture_2")
        time.sleep(1)
        can_process = True
        while True:
            loop()
    except KeyboardInterrupt:
        print(" Program terminated by user. Exiting")
        exit(0)
    except TclError:
        print("Window closed. Exiting")
        exit(0)