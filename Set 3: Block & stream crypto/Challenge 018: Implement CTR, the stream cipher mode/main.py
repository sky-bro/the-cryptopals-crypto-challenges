import struct
import base64
from Crypto.Cipher import AES

class AES_CTR:

    def __init__(self, key, nonce):
        '''
            nonce: 8 bytes
            key: 16 bytes
        '''
        self.cipher = AES.new(key)
        self.BS = 16
        self.nonce = struct.pack('<Q', nonce)

    def _bytes_xor(self, bytes_a, bytes_b):
        result = []
        for i in range(min(len(bytes_a), len(bytes_b))):
            result.append(bytes_a[i] ^ bytes_b[i])
        return bytes(result)

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

def main():
    cipher = AES_CTR('YELLOW SUBMARINE', 0)
    ciphertext = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
    print(ciphertext)
    print(cipher.decrypt(ciphertext))

if __name__ == "__main__":
    main()