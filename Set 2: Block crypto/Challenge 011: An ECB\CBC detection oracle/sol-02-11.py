import os
from Crypto.Cipher import AES
from random import randint


def random_bytes(size=16):
    return os.urandom(size)


class AES_ECB:
    def __init__(self, key, BS=16):
        self.cipher = AES.new(key)
        self.BS = BS

    def _pad(self, s):
        needed_bytes_num = self.BS - len(s) % self.BS
        return s + bytes([needed_bytes_num] * needed_bytes_num)

    def _unpad(self, s):
        return s[:-s[-1]]

    def encrypt(self, p):
        p = self._pad(p)
        result = b''
        for i in range(0, len(p), self.BS):
            result += self.cipher.encrypt(p[i:i+self.BS])
        return result

    def decrypt(self, c):
        result = b''
        for i in range(0, len(c), self.BS):
            result += self.cipher.decrypt(c[i:i+self.BS])
        return self._unpad(result)


class AES_CBC:
    def __init__(self, key, iv=b'\x00'*16, BS=16):
        self.cipher = AES.new(key)
        self.IV = iv
        self.BS = BS

    def _pad(self, s):
        needed_bytes_num = self.BS - len(s) % self.BS
        return s + bytes([needed_bytes_num] * needed_bytes_num)

    def _unpad(self, s):
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
        return result

    def decrypt(self, c):
        chain_blk = self.IV
        result = b''
        for i in range(0, len(c), self.BS):
            result += self._bytes_xor(
                self.cipher.decrypt(c[i:i+self.BS]), chain_blk)
            chain_blk = c[i:i+self.BS]
        return self._unpad(result)


def encryption_oracle(p):
    p = os.urandom(randint(5, 10)) + p + os.urandom(randint(5, 10))
    print('Plaintext:', p)
    k = random_bytes(16)
    cipher = None
    if os.urandom(1)[0] >> 7:
        print('Oracle: cbc mode')
        cipher = AES_CBC(k, iv=random_bytes(16))
    else:
        print('Oracle: ecb mode')
        cipher = AES_ECB(k)
    c = cipher.encrypt(p)
    print('Ciphertext:', c)
    return c


def distinguisher(c, BS=16):
    blks = []
    for i in range(0, len(c), BS):
        blks.append(c[i:i+BS])
    if len(blks) == len(set(blks)):
        print('Adversary: cbc mode\n')
    else:
        print('Adversary: ecb mode\n')


def main():
    for i in range(10):
        # make sure that blk repeats
        # print('Plaintext:', b'abc'+bytes([i]))
        distinguisher(encryption_oracle(b'a'*(11+16+16)+bytes([i])))


if __name__ == "__main__":
    main()
