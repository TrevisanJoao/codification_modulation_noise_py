import numpy as np

def generate_manchester_signal(string):
    bits = np.array([int(bit) for bit in string])
    signal = []
    for bit in bits:
        if bit == 0:
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])
    return np.array(signal)

def generate_nrz_polar_signal(string):
    bits = np.array([int(bit) for bit in string])
    signal = []
    for bit in bits:
        if bit == 0:
            signal.append(-1)
        else:
            signal.append(1)
    return np.array(signal)