import numpy as np

def ascii_to_binary(text: str) -> str:
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_ascii(binary: np.ndarray) -> str:
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        if len(byte) < 8:
            break
        byte_value = int(''.join(str(int(bit)) for bit in byte), 2)
        text += chr(byte_value)

    return text