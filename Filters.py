import numpy as np
import scipy.signal as signal

# Digital filter forward and backward
def digital(x, n=30, a=1):
    b = [1. / n] * n
    y = signal.filtfilt(b, a, x, padlen = 0)
    return y

# One-dimensional filter with an IIR or FIR filter
def iir(x, n=20, a=1):
    b = [1. / n] * n
    b, a = signal.butter(2, 0.01)

    zi = signal.lfilter_zi(b, a) 
    y, _ = signal.lfilter(b, a, x, zi = zi * x[0])
    return y

# Savitzky-Golay filter filter
def savgol(x):
    return signal.savgol_filter(x, 201, 1)

# Rolling average 
def rolling(x, window = 20):
    return x.rolling(window = window).mean()
