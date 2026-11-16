def ascii_to_binary(text: str) -> str:
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_ascii(binary: str) -> str:
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text