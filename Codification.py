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
def decode_manchester_signal(signal):
    signal = np.array(signal)
    decoded = []

    for i in range(0, len(signal), 2):
        pair = signal[i:i + 2]

        if len(pair) < 2:
            break

        if pair[0] == 1 and pair[1] == -1:
            decoded.append(0)
        elif pair[0] == -1 and pair[1] == 1:
            decoded.append(1)
        else:
            decoded.append(-1)

    return np.array(decoded)

def generate_nrz_polar_signal(string):
    bits = np.array([int(bit) for bit in string])
    signal = []
    for bit in bits:
        if bit == 0:
            signal.append(-1)
        else:
            signal.append(1)
    return np.array(signal)
def decode_nrz_polar_signal(signal):
    signal = np.array(signal)
    decoded = []

    for level in signal:
        if level == -1:
            decoded.append(0)
        elif level == 1:
            decoded.append(1)
        else:
            decoded.append(-1)

    return np.array(decoded)