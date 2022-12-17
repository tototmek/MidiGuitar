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
freq_divisor = 32
buff_multiplier = 32

can_process = False

batch_size = blocksize / freq_divisor
signal_length = int(blocksize * buff_multiplier / freq_divisor)
signal = np.ndarray(signal_length)
signal_samplerate = client.samplerate / freq_divisor
print("Signal length:\t\t", signal_length)
print("Signal samplerate:\t", signal_samplerate)

note_detector = note_detection.NoteDetector("/home/tototmek/Projects/MidiGuitar/config/notes.yaml")

@client.set_process_callback
def process(frames):
    data = in_port.get_array()[::freq_divisor]
    for i in range(buff_multiplier-1):
        signal[int(i*batch_size):int(i*batch_size+batch_size)] = signal[int((i+1)*batch_size):int((i+1)*batch_size+batch_size)]
    signal[int(-1-batch_size):-1] = data
    if (can_process):
        xf, yf = signal_processing.fft(signal[0:-1], signal_length-1, 1 / signal_samplerate)
        peaks = signal_processing.get_peaks(xf, yf, 2)
        notes = note_detector.get_notes_from_peaks(peaks)
        if notes:
            print(notes)

def loop():
    xf, yf = signal_processing.fft(signal[0:-1], signal_length-1, 1 / signal_samplerate)
    peaks = signal_processing.get_peaks(xf, yf, 2)
    plt.subplot(2, 1, 1)
    plt.clf()
    plt.plot(xf, yf)
    unzipped_peaks = list(zip(*peaks))
    if unzipped_peaks:
        plt.scatter(unzipped_peaks[0], unzipped_peaks[1])
    for note in note_detector._data["notes"]:
        plt.scatter([note["frequency"]], [note["amplitude"]])
    plt.ylim(0, 30)
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