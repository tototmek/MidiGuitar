import numpy as np
from scipy.fft import rfft, rfftfreq


def fft(signal, length, inverse_samplerate):
    """
    Calculates FFT of the given signal\n
    returns (xf, yf) - frequencies and corresponding amplitudes
    """
    yf = np.abs(rfft(signal))
    xf = rfftfreq(length, inverse_samplerate)
    return (xf, yf)

def get_peaks(xf, yf, threshold = 5):
    """
    Locates the peaks in fft output\n
    returns a list of (frequency, amplitude) pairs of peaks
    """
    peaks = []
    length = len(xf)
    assert length == len(yf)
    for i in range(1, length-1):
        if yf[i] < threshold:
            continue
        if yf[i] > yf[i-1] and yf[i] > yf[i+1]:
            peaks.append((xf[i], yf[i]))
    return peaks
