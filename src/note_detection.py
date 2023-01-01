import logger
import numpy as np  

#use autocorrelation to find the pitch of a signal
def detect_pitch(signal, samplerate, freq_range):

    #find the autocorrelation of the signal
    autocorrelation = np.correlate(signal, signal, mode='full')
    # find first two peaks
    peaks = np.argpartition(autocorrelation, -2)[-2:]
    # find the difference between the peaks
    peak_diff = peaks[1] - peaks[0]
    # find the frequency of the difference
    freq = samplerate / peak_diff
    print(freq)
    # check if the frequency is within the range
    if freq_range[0] <= freq <= freq_range[1]:
        return freq
    else:
        return 0
        