import sys
import base64
from Crypto.Cipher import AES

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
            chain_blk = self.cipher.encrypt(self._bytes_xor(chain_blk, p[i:i+self.BS]))
            result += chain_blk
        return result

    def decrypt(self, c):
        chain_blk = self.IV
        result = b''
        for i in range(0, len(c), self.BS):
            result += self._bytes_xor(self.cipher.decrypt(c[i:i+self.BS]), chain_blk)
            chain_blk = c[i:i+self.BS]
        return self._unpad(result)

def main():
    # cipher = AES_CBC('a'*16)
    # c = cipher.encrypt(b'abc')
    # print(cipher.decrypt(c))
    # return
    cipher = AES_CBC("YELLOW SUBMARINE")
    f = open('10.txt')
    c = base64.b64decode(f.read())
    p = cipher.decrypt(c)
    print(p.decode())


if __name__ == "__main__":
    main()