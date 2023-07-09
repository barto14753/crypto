import crypto.utils as utils
import numpy as np
import binascii

class MD5:
    LENGTH_BITS = 64
    BLOCK_SIZE = 512
    
    shift = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    K = [ 
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 
    ]

    def __init__(self, data):
        self.data = data
        self.hash_value = MD5.md5(data)

    def data(self):
        return self.data
    
    def hash(self):
        return self.hash_value

    def md5(data):
        bits = utils.str_to_bits(data)
        bits_len = len(bits)
        bits = MD5.add_padding(bits)
        bits = MD5.add_length_bits(bits, bits_len)
        blocks = utils.split_512_blocks(bits)
        a0 = utils.int_to_32_bits(0x67452301)
        b0 = utils.int_to_32_bits(0xefcdab89)
        c0 = utils.int_to_32_bits(0x98badcfe)
        d0 = utils.int_to_32_bits(0x10325476)
        var = (a0, b0, c0, d0)
        for block in blocks:
            var = MD5.process_block(block, var)
        bits = np.concatenate(var)
        bits = np.ascontiguousarray(bits)
        hash_bytes = np.packbits(bits)
        hash_bytes = np.flip(hash_bytes).copy(order='C')
        return binascii.hexlify(hash_bytes).decode()
    
    def process_block(block_512, var):
        A, B, C, D = var
        a0, b0, c0, d0 = A, B, C, D
        M = utils.split_32_blocks(block_512)
        E, g = 0, 0
        for i in range(64):
            if i < 16:
                E = MD5.F(B, C, D)
                g = i
            elif i < 32:
                E = MD5.G(B, C, D)
                g = (5*i + 1) % 16
            elif i < 48:
                E = MD5.H(B, C, D)
                g = (3*i + 5) % 16
            elif i < 64:
                E = MD5.I(B, C, D)
                g = (7*i) % 16
            temp = D
            D = C
            C = B
            A = MD5.add_modulo(A, E)
            A = MD5.add_modulo(A, utils.int_to_32_bits(MD5.K[i]))
            A = MD5.add_modulo(A, utils.make_little_endian(M[g]))
                
            A = utils.left_rotate(A, MD5.shift[i])
            B = MD5.add_modulo(B, A)
            A = temp
        a0 = MD5.add_modulo(a0, A)
        b0 = MD5.add_modulo(b0, B)
        c0 = MD5.add_modulo(c0, C)
        d0 = MD5.add_modulo(d0, D)
        return (d0, c0, b0, a0)


    def add_padding(bits: np.ndarray) -> np.ndarray:
        bits_len = len(bits)
        padding_len = MD5.BLOCK_SIZE - (bits_len + MD5.LENGTH_BITS + 1) % MD5.BLOCK_SIZE
        one_padding = np.ones(1)
        padding = np.zeros(padding_len)
        bits_with_one_padding = np.append(bits, one_padding)
        bits_with_padding = np.append(bits_with_one_padding, padding)
        return bits_with_padding

    def add_length_bits(bits: np.ndarray, bits_len: int) -> np.ndarray:
        length_bits = utils.int_to_64_bits(bits_len)
        little_endian_length_bits = utils.make_little_endian(length_bits)
        bits_with_length = np.append(bits, little_endian_length_bits)
        return bits_with_length

    def left_rotate(arr, rotations):
        rotations = rotations % arr.size
        return np.roll(arr, -rotations)

    def add(a_bits, b_bits):
        a = utils.bits_to_int(a_bits)
        b = utils.bits_to_int(b_bits)
        res = (a + b)
        return utils.int_to_32_bits(res)

    def add_modulo(a_bits, b_bits):
        a = utils.bits_to_int(a_bits)
        b = utils.bits_to_int(b_bits)
        res = (a + b) & 0xFFFFFFFF
        return utils.int_to_32_bits(res)

    def F(K, L, M) -> np.ndarray:
        return (K & L) | (utils.binary_negation(K) & M)

    def G(K, L, M) -> np.ndarray:
        return (M & K) | (utils.binary_negation(M) & L)

    def H(K, L, M) -> np.ndarray:
        return  K ^ L ^ M

    def I(K, L, M) -> np.ndarray:
        return L ^ (K | utils.binary_negation(M))
    