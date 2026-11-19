import numpy as np

def generate_ASK_modulated_signal(string):
    bits = np.array(string)
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
def demodulate_ASK_signal(signal):
    signal = np.array(signal)

    amplitude = 1
    frequency = 5
    samples_per_bit = 500
    decoded = []

    for i in range(0, len(signal), samples_per_bit):
        wave = signal[i:i + samples_per_bit]

        if len(wave) < samples_per_bit:
            break

        t = np.linspace(0, 1, samples_per_bit, endpoint=False)

        reference = np.sin(2 * np.pi * frequency * t)

        correlation = 2 * np.mean(wave * reference)

def generate_QPSK_modulated_signal(string):
    bits = np.array(string)

    amplitude = 1
    frequency = 5
    samples_per_symbol = 500

    signal = []

    # Ensure an even number of elements
    if len(bits) % 2 != 0:
        bits = np.append(bits, 1)

    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i + 1]

        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)

        # QPSK phase mapping
        if bit1 == -1 and bit2 == -1:
            phase = np.pi / 4
        elif bit1 == -1 and bit2 == 1:
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
def demodulate_QPSK_signal(signal):
    signal = np.array(signal)

    frequency = 5
    samples_per_symbol = 500
    decoded = []

    for i in range(0, len(signal), samples_per_symbol):
        wave = signal[i:i + samples_per_symbol]

        if len(wave) < samples_per_symbol:
            break

        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)

        sin_reference = np.sin(2 * np.pi * frequency * t)
        cos_reference = np.cos(2 * np.pi * frequency * t)

        sin_component = 2 * np.mean(wave * sin_reference)
        cos_component = 2 * np.mean(wave * cos_reference)

        if sin_component >= 0 and cos_component >= 0:
            decoded.extend([-1, -1])
        elif sin_component < 0 and cos_component >= 0:
            decoded.extend([-1, 1])
        elif sin_component < 0 and cos_component < 0:
            decoded.extend([1, 1])
        else:
            decoded.extend([1, -1])

    return np.array(decoded)




def generate_BPSK_modulated_signal(string):
    bits = np.array(string)
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
def demodulate_BPSK_signal(signal):
    signal = np.array(signal)

    amplitude = 1
    frequency = 5
    samples_per_bit = 500
    decoded = []

    for i in range(0, len(signal), samples_per_bit):
        wave = signal[i:i + samples_per_bit]

        if len(wave) < samples_per_bit:
            break

        t = np.linspace(0, 1, samples_per_bit, endpoint=False)

        reference = np.sin(2 * np.pi * frequency * t)

        correlation = 2 * np.mean(wave * reference)

        if correlation >= 0:
            decoded.append(1)
        else:
            decoded.append(-1)

    return np.array(decoded)

def generate_16QAM_modulated_signal(string):
    bits = np.array(string)
    amplitude = 1
    frequency = 5
    samples_per_symbol = 500
    signal = []

    if len(bits) % 4 != 0:
        bits = np.append(bits, [1] * (4 - (len(bits) % 4)))

    gray_mapping = {
        (-1, -1): -3,
        (-1, 1): -1,
        (1, 1): 1,
        (1, -1): 3
    }

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
def demodulate_16QAM_signal(signal):
    signal = np.array(signal)

    frequency = 5
    samples_per_symbol = 500
    decoded = []

    gray_mapping = {
        -3: (-1, -1),
        -1: (-1, 1),
        1: (1, 1),
        3: (1, -1)
    }

    levels = np.array([-3, -1, 1, 3])

    for i in range(0, len(signal), samples_per_symbol):
        wave = signal[i:i + samples_per_symbol]

        if len(wave) < samples_per_symbol:
            break

        t = np.linspace(0, 1, samples_per_symbol, endpoint=False)

        cos_reference = np.cos(2 * np.pi * frequency * t)
        sin_reference = np.sin(2 * np.pi * frequency * t)

        i_component = 2 * np.sqrt(18) * np.mean(wave * cos_reference)
        q_component = -2 * np.sqrt(18) * np.mean(wave * sin_reference)

        i_value = levels[np.argmin(np.abs(levels - i_component))]
        q_value = levels[np.argmin(np.abs(levels - q_component))]

        decoded.extend(gray_mapping[i_value])
        decoded.extend(gray_mapping[q_value])

    return np.array(decoded)