import crypto.utils as utils
import numpy as np

class Base64:
    TABLE = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '+', '/'
    ]

    def __init__(self, data):
        self.data = data
        self.encoded_data = Base64.encode(data)

    def data(self):
        return self.data
    
    def encoded_data(self):
        return self.encoded_data

    def encode(string: str) -> str:
        assert len(string) > 0
        pad_len = (3 - (len(string) % 3)) % 3 
        bits = utils.str_to_bits(string)
        if len(string) % 3 > 0:
            bits = Base64.add_padding(bits)
        sextets = utils.split_to_sextets(bits)
        result = "".join(Base64.TABLE[utils.bits_to_int(sextet)] for sextet in sextets)
        result += pad_len * "="
        return result
    
    def decode(base64_string: str) -> str:
        assert len(base64_string) > 0
        base64_string = base64_string.replace('=', '')
        bits = np.array([])
        for ch in base64_string:
            index = Base64.TABLE.index(ch)
            bits = np.append(bits, utils.int_to_x_bits(index, 6))
        octets = utils.split_to_octets(bits)
        result = "".join(utils.bits_to_str(octet) for octet in octets)
        return result

    def add_padding(bits: np.ndarray) -> np.ndarray:
        length = 6 - len(bits) % 6
        return np.append(bits, np.zeros(length))