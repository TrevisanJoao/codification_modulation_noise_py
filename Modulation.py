import numpy as np

def generate_ASK_modulated_signal(string):
    bits = np.array([int(bit) for bit in string])
    amplitude = 1
    frequency = 5
    samples_per_bit = 500
    signal = []
    for bit in bits:
        t = np.linspace(0, 1, samples_per_bit, endpoint=False)
        if bit == 1:
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        else:
            wave = np.zeros(samples_per_bit)
        signal.extend(wave)
    return np.array(signal)



import numpy as np

def generate_QPSK_modulated_signal(string):
    bits = np.array([int(bit) for bit in string])
    amplitude = 1
    frequency = 5
    samples_per_symbol = 500
    signal = []

    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)
    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i + 1]
        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)

        if bit1 == 0 and bit2 == 0:
            phase = np.pi / 4
        elif bit1 == 0 and bit2 == 1:
            phase = 3 * np.pi / 4
        elif bit1 == 1 and bit2 == 1:
            phase = 5 * np.pi / 4
        else:
            phase = 7 * np.pi / 4
        wave = amplitude * np.sin(
            2 * np.pi * frequency * t + phase
        )
        signal.extend(wave)

    return np.array(signal)


import numpy as np

def generate_QPSK_modulated_signal(string):
    bits = np.array([int(bit) for bit in string])

    amplitude = 1
    frequency = 5
    samples_per_symbol = 500

    signal = []

    # Ensure an even number of bits
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)

    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i + 1]

        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)

        # QPSK phase mapping
        if bit1 == 0 and bit2 == 0:
            phase = np.pi / 4
        elif bit1 == 0 and bit2 == 1:
            phase = 3 * np.pi / 4
        elif bit1 == 1 and bit2 == 1:
            phase = 5 * np.pi / 4
        else:
            phase = 7 * np.pi / 4

        wave = amplitude * np.sin(
            2 * np.pi * frequency * t + phase
        )

        signal.extend(wave)

    return np.array(signal)


def generate_BPSK_modulated_signal(string):
    bits = np.array([int(bit) for bit in string])
    amplitude = 1
    frequency = 5
    samples_per_bit = 500
    signal = []

    for bit in bits:
        t = np.linspace(0, 1, samples_per_bit, endpoint=False)
        if bit == 1:
            phase = 0
        else:
            phase = np.pi
        wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        signal.extend(wave)

    return np.array(signal)


def generate_16QAM_modulated_signal(string):
    bits = np.array([int(bit) for bit in string])
    amplitude = 1
    frequency = 5
    samples_per_symbol = 500
    signal = []

    if len(bits) % 4 != 0:
        bits = np.append(bits, [0] * (4 - (len(bits) % 4)))

    gray_mapping = {(0, 0): -3, (0, 1): -1, (1, 1): 1, (1, 0): 3}

    for i in range(0, len(bits), 4):
        i_value = gray_mapping[(int(bits[i]), int(bits[i + 1]))]
        q_value = gray_mapping[(int(bits[i + 2]), int(bits[i + 3]))]
        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)
        wave = amplitude * (
            i_value * np.cos(2 * np.pi * frequency * t)
            - q_value * np.sin(2 * np.pi * frequency * t)
        ) / np.sqrt(18)
        signal.extend(wave)

    return np.array(signal)



