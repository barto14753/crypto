import crypto.utils as utils
import numpy as np
import binascii

class SHA1:
    LENGTH_BITS = 64
    BLOCK_SIZE = 512

    def __init__(self, data):
        self.data = data
        self.hash_value = SHA1.sha1(data)

    def data(self):
        return self.data
    
    def hash(self):
        return self.hash_value
    
    def sha1(data):
        bits = utils.str_to_bits(data)
        bits_len = len(bits)
        bits = SHA1.add_padding(bits)
        bits = SHA1.add_length_bits(bits, bits_len)
        blocks = utils.split_512_blocks(bits)

        h0 = utils.int_to_32_bits(0x67452301)
        h1 = utils.int_to_32_bits(0xEFCDAB89)
        h2 = utils.int_to_32_bits(0x98BADCFE)
        h3 = utils.int_to_32_bits(0x10325476)
        h4 = utils.int_to_32_bits(0xC3D2E1F0)
        var = (h0, h1, h2, h3, h4)

        for block in blocks:
            var = SHA1.process_block(block, var)
        
        h0, h1, h2, h3, h4 = var
        bits = h0
        bits = np.append(bits, h1)
        bits = np.append(bits, h2)
        bits = np.append(bits, h3)
        bits = np.append(bits, h4)
        hash_bytes = np.packbits(bits)
        return binascii.hexlify(hash_bytes).decode()

    def add_padding(bits: np.ndarray) -> np.ndarray:
        bits_len = len(bits)
        padding_len = SHA1.BLOCK_SIZE - (bits_len + SHA1.LENGTH_BITS + 1) % SHA1.BLOCK_SIZE
        one_padding = np.ones(1)
        padding = np.zeros(padding_len)
        bits_with_one_padding = np.append(bits, one_padding)
        bits_with_padding = np.append(bits_with_one_padding, padding)
        return bits_with_padding

    def add_length_bits(bits: np.ndarray, bits_len: int) -> np.ndarray:
        length_bits = utils.int_to_64_bits(bits_len)
        bits_with_length = np.append(bits, length_bits)
        return bits_with_length
    
    def add_modulo(a_bits, b_bits):
        a = utils.bits_to_int(a_bits)
        b = utils.bits_to_int(b_bits)
        res = (a + b) & 0xFFFFFFFF
        return utils.int_to_32_bits(res)
    
    def extend_chunks(chunks: np.ndarray) -> np.ndarray:
        for i in range(16, 80):
            new_chunk = chunks[i-3] ^ chunks[i-8] ^ chunks[i-14] ^ chunks[i-16]
            new_chunk = utils.left_rotate(new_chunk, 1)
            chunks = np.append(chunks, [new_chunk], axis=0)
        return chunks

    def process_block(block, var):
        chunks =  utils.split_32_blocks(block)
        chunks = SHA1.extend_chunks(chunks)

        a, b, c, d, e = var
        h0, h1, h2, h3, h4 = a, b, c, d, e

        for i, chunk in enumerate(chunks):
            if i < 20:
                f = (b & c) | (utils.binary_negation(b) & d)
                k = utils.int_to_32_bits(0x5A827999)
            elif i < 40:
                f = b ^ c ^ d
                k = utils.int_to_32_bits(0x6ED9EBA1)
            elif i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = utils.int_to_32_bits(0x8F1BBCDC)
            elif i < 80:
                f = b ^ c ^ d
                k = utils.int_to_32_bits(0xCA62C1D6)

            tmp = SHA1.add_modulo(utils.left_rotate(a, 5), f)
            tmp = SHA1.add_modulo(tmp, e)
            tmp = SHA1.add_modulo(tmp, k)
            tmp = SHA1.add_modulo(tmp, chunk)
            e = d
            tmp_c = c
            c = utils.left_rotate(b, 30)
            b = a
            a = tmp
            d = tmp_c
        
        h0 = SHA1.add_modulo(h0, a)
        h1 = SHA1.add_modulo(h1, b)
        h2 = SHA1.add_modulo(h2, c)
        h3 = SHA1.add_modulo(h3, d)
        h4 = SHA1.add_modulo(h4, e)

        return (h0, h1, h2, h3, h4)
    
