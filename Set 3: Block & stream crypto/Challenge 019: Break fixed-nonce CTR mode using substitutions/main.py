import os
import struct
import base64
import string
from Crypto.Cipher import AES

def bytes_xor(bytes_a, bytes_b):
    return bytes([a^b for a, b in zip(bytes_a, bytes_b)])

class AES_CTR:

    def __init__(self, key, nonce=0):
        '''
            nonce: 8 bytes
            key: 16 bytes
        '''
        self.cipher = AES.new(key)
        self.BS = 16
        self.nonce = struct.pack('<Q', nonce)

    def _bytes_xor(self, bytes_a, bytes_b):
        return bytes([a^b for a, b in zip(bytes_a, bytes_b)])

    def encrypt(self, plaintext):
        ctr = 0
        result = b''
        for i in range(0, len(plaintext), self.BS):
            pad = self.nonce + struct.pack('<Q', ctr)
            pad = self.cipher.encrypt(pad)
            result += self._bytes_xor(pad, plaintext[i:i+self.BS])
            ctr += 1
        return result

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)

random_key = os.urandom(16)

cipher = AES_CTR(random_key)

def get_ciphertexts():
    with open('./base64_plaintexts.txt', 'r') as f:
        plaintexts = f.readlines()
    # print([base64.b64decode(x) for x in plaintexts])
    ciphertexts = [cipher.encrypt(base64.b64decode(x)) for x in plaintexts if x.strip() != '']
    return ciphertexts

freq_exp = {
    'e': .1202, 't': .0910, 'a': .0812, 'o': .0768, 
    'i': .0731, 'n': .0695, 's': .0628, 'r': .0602, 
    'h': .0592, 'd': .0432, 'l': .0398, 'u': .0288, 
    'c': .0271, 'm': .0261, 'f': .0230, 'y': .0211, 
    'w': .0209, 'g': .0203, 'p': .0182, 'b': .0149, 
    'v': .0111, 'k': .0069, 'x': .0017, 'q': .0011, 
    'j': .0010, 'z': .0007
}

def get_dist2eng(english_text):
    count = {}
    ignored = 0
    for i in range(26):
        count[i] = 0
    for c in english_text:
        if c >= 0x41 and c <= 0x5a:
            count[c - 0x41] += 1
        elif c >= 0x61 and c <= 0x7a:
            count[c - 0x61] += 1
        elif c in b'\':;,.!?-0123456789 \r\t\n':
            ignored += 1
        else:
            # print(ch)
            return -1
    chi2 = 0
    letter_len = len(english_text) - ignored
    if letter_len == 0:
        return 1
    for i in range(26):
        observed = count[i]
        expected = letter_len * freq_exp[chr(i + 0x61)]
        difference = observed - expected
        chi2 += difference**2/expected
    return chi2

def guess_stream_key(ciphertexts, max_len, adjustment=None):
    stream_key = []
    for i in range(max_len):
        kis = [] 
        for ki in range(256):
            eng_text = []
            for c in ciphertexts:
                if i < len(c):
                    eng_text.append(ki ^ c[i])
            englishness = get_dist2eng(bytes(eng_text))
            if englishness != -1:
                kis.append((ki, englishness))
        kis.sort(key=lambda pair: pair[1])
        try:
            stream_key.append(kis[0][0])
        except:
            pass
    # wrong adjustment
    # if adjustment:
    #     for i in adjustment:
    #         stream_key[i] = adjustment[i]
    return bytes(stream_key)

def main():
    ciphertexts = get_ciphertexts()
    
    max_len = max([len(c) for c in ciphertexts])
    # adjustment = {}
    stream_key = guess_stream_key(ciphertexts, max_len)
    print(stream_key, len(stream_key))
    plaintexts = [bytes_xor(stream_key, c) for c in ciphertexts]
    for p in plaintexts:
        print(p)
    # print(plaintexts)

if __name__ == "__main__":
    main()