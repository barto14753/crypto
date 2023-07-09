import numpy as np

def str_to_bits(string: str) -> np.ndarray:
    bytes_array = bytes(string, 'utf-8')
    array = np.frombuffer(bytes_array, dtype=np.uint8)
    bits_array = np.unpackbits(array)
    return bits_array

def int_to_x_bits(number: int, bits) -> np.ndarray:
    binary_string = np.binary_repr(number, width=bits)
    return np.array(list(binary_string), dtype=np.uint8)

def int_to_64_bits(number: int) -> np.ndarray:
    return int_to_x_bits(number, 64)

def int_to_32_bits(number: int) -> np.ndarray:
    return int_to_x_bits(number, 32)

def bits_to_int(bits_array):
    binary_string = ''.join(bits_array.astype(str))
    return int(binary_string, 2)

def binary_negation(bits: np.ndarray) -> np.ndarray:
    return np.vectorize(lambda x: (x + 1) % 2)(bits)

def split_x_blocks(bits: np.ndarray, size: int) -> np.ndarray:
    assert bits.size % size == 0
    num_blocks = bits.size // size
    blocks = np.array_split(bits, num_blocks)
    return np.array(blocks, dtype=np.uint8)

def split_512_blocks(bits: np.ndarray) -> np.ndarray:
    return split_x_blocks(bits, 512)

def split_32_blocks(bits: np.ndarray) -> np.ndarray:
    return split_x_blocks(bits, 32)

def left_rotate(arr, rotations):
    rotations = rotations % arr.size
    return np.roll(arr, -rotations)

def add_modulo(a_bits, b_bits):
    a = bits_to_int(a_bits)
    b = bits_to_int(b_bits)
    res = (a + b) & 0xFFFFFFFF
    return int_to_32_bits(res)

def bits_to_str(bits: np.ndarray) -> str:
    bits_array = np.packbits(bits)
    return bits_array.tobytes().decode('ascii')

def split_to_sextets(bits: np.ndarray) -> np.ndarray:
    num_blocks = bits.size // 6
    blocks = np.array_split(bits, num_blocks)
    return np.array(blocks, dtype=np.uint8)

def split_to_octets(bits: np.ndarray) -> np.ndarray:
    num_full_subarrays = len(bits) // 8
    subarrays = []
    for i in range(num_full_subarrays):
        subarrays.append(np.array(bits[i * 8: (i + 1) * 8], dtype=np.uint8))
    return subarrays

def rotate_x_parts(bits: np.ndarray, x: int) -> np.ndarray:
    split_arr = np.array_split(bits, x)
    reversed_arr = np.flip(split_arr, 0)
    return np.concatenate(reversed_arr)

def rotate_4_parts(bits: np.ndarray) -> np.ndarray:
    return rotate_x_parts(bits, 4)

def rotate_2_parts(bits: np.ndarray) -> np.ndarray:
    return rotate_x_parts(bits, 2)

def make_little_endian(bits: np.ndarray) -> np.ndarray:
    assert bits.size % 8 == 0
    split_arr = np.array_split(bits, bits.size // 8)
    reversed_arr = np.flip(split_arr, 0)
    return np.concatenate(reversed_arr)
