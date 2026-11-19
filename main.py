import Codification
import from_to_binary
import Modulation
import channel



def main():
    message = "Hello World!"
    modulation = "BPSK"
    snr_db = 20

    # Transmitter
    binary = from_to_binary.ascii_to_binary(message)
    encoded = Codification.generate_nrz_polar_signal(binary)
    modulated = Modulation.generate_BPSK_modulated_signal(encoded)

    spectral_efficiency = channel.calculate_spectral_efficiency(modulation)

    # ==============================
    # TEST 1: AWGN CHANNEL
    # ==============================

    received_awgn = channel.simulate_AWGN_channel(modulated, snr_db)
    demodulated_awgn = Modulation.demodulate_BPSK_signal(received_awgn)
    decoded_awgn = Codification.decode_nrz_polar_signal(demodulated_awgn)
    recovered_awgn = from_to_binary.binary_to_ascii(decoded_awgn)

    ber_awgn = channel.calculate_BER(binary, decoded_awgn)

    # ==============================
    # TEST 2: BURST NOISE CHANNEL
    # ==============================

    received_burst = channel.simulate_burst_noise_channel(
        modulated,
        noise_power=2.0,
        burst_probability=0.001,
        burst_length=500
    )

    demodulated_burst = Modulation.demodulate_BPSK_signal(received_burst)
    decoded_burst = Codification.decode_nrz_polar_signal(demodulated_burst)
    recovered_burst = from_to_binary.binary_to_ascii(decoded_burst)

    ber_burst = channel.calculate_BER(binary, decoded_burst)

    # ==============================
    # RESULTS
    # ==============================

    print("\n========== TRANSMISSION INFORMATION ==========")

    print("Original message:      ", message)
    print("Binary:                ", binary)
    print("Number of bits:        ", len(binary))
    print("Modulation:            ", modulation)
    print("Modulated samples:     ", len(modulated))

    print("\n========== AWGN CHANNEL ==========")

    print("SNR:                   ", snr_db, "dB")
    print("Received samples:      ", len(received_awgn))
    print("Recovered message:     ", recovered_awgn)
    print(f"BER:                    {ber_awgn:.6f}")
    print("Spectral efficiency:   ", spectral_efficiency, "bits/s/Hz")
    print("Transmission successful:", message == recovered_awgn)

    print("\n========== BURST NOISE CHANNEL ==========")

    print("Noise power:           ", 2.0)
    print("Burst probability:     ", 0.001)
    print("Burst length:          ", 500)
    print("Received samples:      ", len(received_burst))
    print("Recovered message:     ", recovered_burst)
    print(f"BER:                    {ber_burst:.6f}")
    print("Spectral efficiency:   ", spectral_efficiency, "bits/s/Hz")
    print("Transmission successful:", message == recovered_burst)

    print("\n========== COMPARISON ==========")

    print(f"AWGN BER:              {ber_awgn:.6f}")
    print(f"Burst Noise BER:       {ber_burst:.6f}")


if __name__ == "__main__":
    main()


