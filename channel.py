import numpy as np

def simulate_AWGN_channel(signal, snr_db):
    signal = np.array(signal)

    signal_power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear

    noise = np.random.normal(
        0,
        np.sqrt(noise_power),
        len(signal)
    )

    return signal + noise

def simulate_burst_noise_channel(signal, noise_power=1.0, burst_probability=0.01, burst_length=500):
    signal = np.array(signal)
    noisy_signal = signal.copy()
    i = 0

    while i < len(signal):
        if np.random.random() < burst_probability:
            end = min(i + burst_length, len(signal))

            noise = np.random.normal(
                0,
                np.sqrt(noise_power),
                end - i
            )
            noisy_signal[i:end] += noise

            i = end
        else:
            i += 1

    return noisy_signal


def calculate_BER(transmitted_bits, received_bits):
    transmitted_bits = np.array([int(bit) for bit in transmitted_bits])
    received_bits = np.array(received_bits).flatten()

    if len(transmitted_bits) != len(received_bits):
        raise ValueError("The bit sequences must have the same length.")

    if len(transmitted_bits) == 0:
        return 0

    errors = np.sum(transmitted_bits != received_bits)
    total_bits = len(transmitted_bits)

    return errors / total_bits

def calculate_spectral_efficiency(modulation):
    efficiencies = {
        "ASK": 1,
        "BPSK": 1,
        "QPSK": 2,
        "16QAM": 4
    }

    return efficiencies.get(modulation.upper(), None)