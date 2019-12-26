import os
from Crypto.Cipher import AES


def random_bytes(size=16):
    return os.urandom(size)


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


k = random_bytes(16)
cipher = AES_CBC(k, iv=random_bytes(16))


def encrypt_oracle(userdata):
    p = b"comment1=cooking%20MCs;userdata=" + userdata + b";comment2=%20like%20a%20pound%20of%20bacon"
    return cipher.encrypt(p)

def check_admin(ciphertext):
    p = cipher.decrypt(ciphertext)
    print(p)
    for pair in p.split(b';'):
        pair = pair.split(b'=')
        print("{}: {}".format(pair[0], pair[1]))
    
def bytes_xor(bytes_a, bytes_b):
    result = [a^b for (a,b) in zip(bytes_a, bytes_b)]
    return bytes(result)

def main():
    # p1 = b'comment1=cooking%20MCs;userdata=' # len(p1) = 32
    # p2 = b';comment2=%20like%20a%20pound%20of%20bacon'
    target = b';admin=true' # len(target) = 11
    userdata = b'a'*32
    ciphertext = encrypt_oracle(userdata)
    tmp = bytes_xor(ciphertext[64-11-16:64-16], bytes_xor(b'a'*11, target))
    new_ciphertext = ciphertext[:64-11-16] + tmp + ciphertext[64-16:]
    check_admin(new_ciphertext)

if __name__ == "__main__":
    main()
