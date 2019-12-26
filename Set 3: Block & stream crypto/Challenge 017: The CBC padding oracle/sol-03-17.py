import os
import base64
from random import randint
from Crypto.Cipher import AES
import string

BS = 16

def random_bytes(size=16):
    return os.urandom(size)

class PaddingException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info
    
    def __str__(self):
        return self.error_info


class AES_CBC:
    def __init__(self, key, iv=b'\x00'*16, BS=16):
        self.cipher = AES.new(key)
        self.IV = iv
        self.BS = BS

    def _pad(self, s):
        needed_bytes_num = self.BS - len(s) % self.BS
        return s + bytes([needed_bytes_num] * needed_bytes_num)

    def _unpad(self, s):
        pad_len = s[-1]
        for i in s[-pad_len:]:
            if i != pad_len:
                raise PaddingException('unpad failed, padding error')
        return s[:-s[-1]]

    def _bytes_xor(self, bytes_a, bytes_b):
        result = []
        for i in range(min(len(bytes_a), len(bytes_b))):
            result.append(bytes_a[i] ^ bytes_b[i])
        return bytes(result)

    def encrypt(self, p):
        p = self._pad(p)
        chain_blk = self.IV
        result = b''
        for i in range(0, len(p), self.BS):
            chain_blk = self.cipher.encrypt(
                self._bytes_xor(chain_blk, p[i:i+self.BS]))
            result += chain_blk
        return result, self.IV

    def decrypt(self, c, iv=None):
        chain_blk = self.IV
        if iv:
            chain_blk = iv
        result = b''
        for i in range(0, len(c), self.BS):
            result += self._bytes_xor(
                self.cipher.decrypt(c[i:i+self.BS]), chain_blk)
            chain_blk = c[i:i+self.BS]
        return self._unpad(result)


k = random_bytes(16)
cipher = AES_CBC(k, iv=random_bytes(16))

plaintexts_arr = [
    'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
]

def bytes_xor(bytes_a, bytes_b):
    result = [a^b for (a,b) in zip(bytes_a, bytes_b)]
    return bytes(result)

def decrypt_oracle(ciphertext, iv):
    try:
        cipher.decrypt(ciphertext, iv)
        return True
    except PaddingException:
        return False

def decrytp_one_blk(pre_blk, target_blk, BS=16):
    result = b''
    # 从后往前一次破一个字节，放到result中
    for i in range(1,BS+1):
        left_part = pre_blk[:BS-i]
        right_part = pre_blk[-i:]
        padding = bytes([i])*i
        # very important here, 
        # 这样失败率大约是1/256
        for j in range(2, 256):
            p = bytes([j]) + result
            iv = left_part + bytes_xor(right_part, bytes_xor(p, padding))
            if decrypt_oracle(target_blk, iv):
                result = p
                break
    if len(result) < BS:
        result = b''
        for i in range(1,BS+1):
            left_part = pre_blk[:BS-i]
            right_part = pre_blk[-i:]
            padding = bytes([i])*i
            # very important here, 
            for j in range(256):
                p = bytes([j]) + result
                iv = left_part + bytes_xor(right_part, bytes_xor(p, padding))
                if decrypt_oracle(target_blk, iv):
                    result = p
                    break
    return result

def brk_CBC_padding_oracle(ciphertext, iv, BS=16):
    result = b''
    pre_blk = iv
    for i in range(0, len(ciphertext), BS):
        target_blk = ciphertext[i:i+BS]
        result += decrytp_one_blk(pre_blk, target_blk)
        pre_blk = target_blk
    return result

def main():
    ori_plaintext = base64.b64decode(plaintexts_arr[randint(0, 9)])
    # ori_plaintext = base64.b64decode(plaintexts_arr[7])
    # ori_plaintext = b'1'*15
    print(ori_plaintext)
    ciphertext, iv = cipher.encrypt(ori_plaintext)
    decrypted_plaintext = brk_CBC_padding_oracle(ciphertext, iv)
    print(decrypted_plaintext)

if __name__ == "__main__":
    main()


