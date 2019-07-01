import base64
from Crypto.Cipher import AES

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

def main():
    # cipher = AES_ECB('a'*16)
    # c = cipher.encrypt(b'abc')
    # print(cipher.decrypt(c))
    # return
    f = open('7.txt')
    c = base64.b64decode(f.read())
    aes_ecb = AES_ECB('YELLOW SUBMARINE')
    text = aes_ecb.decrypt(c).decode()
    print(text)

if __name__ == "__main__":
    main()