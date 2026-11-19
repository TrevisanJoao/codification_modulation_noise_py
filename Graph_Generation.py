import matplotlib.pyplot as plt
import numpy as np
import Codification
import Modulation


def _show_or_save(figure, filename):
    if plt.get_backend().lower() == "agg":
        figure.savefig(filename, bbox_inches="tight")
        plt.close(figure)
        print(f"Backend Agg: gráfico salvo em {filename}")
    else:
        plt.show()


def generate_graph_manchester(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."
    for bit in string:
        if bit != '0' and bit != '1':
            return "Invalid input, please enter a binary string."

    bits = [int(bit) for bit in string]
    signal = Codification.generate_manchester_signal(string)
    times = []
    for i in range(len(bits)):
        times.extend([i, i + 0.5])

    times.append(len(bits))
    signal = np.append(signal, signal[-1])
    figure, ax = plt.subplots(figsize=(12, 4))
    ax.step(times, signal, where='post', linewidth=2)
    ax.set_title("Manchester Encoding")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_yticks([-1, 0, 1])
    ax.set_xticks(range(len(bits) + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "manchester.png")
    return None

def generate_graph_NRZ_Polar(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."
    for bit in string:
        if bit != '0' and bit != '1':
            return "Invalid input, please enter a binary string."

    bits = [int(bit) for bit in string]
    signal = Codification.generate_nrz_polar_signal(string)
    times = []
    for i in range(len(bits)):
        times.append(i)

    times.append(len(bits))
    signal = np.append(signal, signal[-1])
    figure, ax = plt.subplots(figsize=(12, 4))
    ax.step(times, signal, where='post', linewidth=2)
    ax.set_title("NRZ-Polar Encoding")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_yticks([-1, 0, 1])
    ax.set_xticks(range(len(bits) + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "nrz_polar.png")
    return None

def generate_graph_ASK(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."

    for i in range(len(string)):
        if string[i] != '0' and string[i] != '1':
            return "Invalid input, please enter a binary string."

    encoded = Codification.generate_nrz_polar_signal(string)
    signal = Modulation.generate_ASK_modulated_signal(encoded)
    times = np.linspace(0, len(string), len(signal), endpoint=False)

    figure, ax = plt.subplots(figsize=(20, 4))
    ax.plot(times, signal, linewidth=1.5)
    ax.set_title("ASK Modulation")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(len(string) + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "ask.png")
    return None


def generate_graph_BPSK(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."

    for i in range(len(string)):
        if string[i] != '0' and string[i] != '1':
            return "Invalid input, please enter a binary string."

    encoded = Codification.generate_nrz_polar_signal(string)
    signal = Modulation.generate_BPSK_modulated_signal(encoded)
    times = np.linspace(0, len(string), len(signal), endpoint=False)

    figure, ax = plt.subplots(figsize=(20, 4))
    ax.plot(times, signal, linewidth=1.5)
    ax.set_title("BPSK Modulation")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(len(string) + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "bpsk.png")
    return None


def generate_graph_QPSK(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."
    for i in range(len(string)):
        if string[i] != '0' and string[i] != '1':
            return "Invalid input, please enter a binary string."

    if len(string) % 2 != 0:
        string += '0'
    encoded = Codification.generate_nrz_polar_signal(string)
    signal = Modulation.generate_QPSK_modulated_signal(encoded)
    number_of_symbols = len(string) // 2
    times = np.linspace(
        0,
        number_of_symbols,
        len(signal),
        endpoint=False
    )

    figure, ax = plt.subplots(figsize=(20, 4))
    ax.plot(times, signal, linewidth=1.5)
    ax.set_title("QPSK Modulation")
    ax.set_xlabel("Time (Symbols)")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(number_of_symbols + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "qpsk.png")
    return None


def generate_graph_16QAM(string):
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."
    for i in range(len(string)):
        if string[i] != '0' and string[i] != '1':
            return "Invalid input, please enter a binary string."

    if len(string) % 4 != 0:
        string += '0' * (4 - (len(string) % 4))
    encoded = Codification.generate_nrz_polar_signal(string)
    signal = Modulation.generate_16QAM_modulated_signal(encoded)
    number_of_symbols = len(string) // 4
    times = np.linspace(
        0,
        number_of_symbols,
        len(signal),
        endpoint=False
    )

    figure, ax = plt.subplots(figsize=(20, 4))
    ax.plot(times, signal, linewidth=1.5)
    ax.set_title("16-QAM Modulation")
    ax.set_xlabel("Time (Symbols)")
    ax.set_ylabel("Amplitude (V)")
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(number_of_symbols + 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    _show_or_save(figure, "16qam.png")
    return None

def enough_bits(string : str) -> str:
    if len(string) < 16:
        return "String is too short, please enter a string with more than 16 characters."
    for bit in string:
        if bit != '0' and bit != '1':
            return "Invalid input, please enter a binary string."
