import os
import sys
import base64
from Crypto.Cipher import AES
from random import randint

def random_bytes(size=16):
    return os.urandom(size)

def print_bytes(bstr):
    for i in range(0, len(bstr), 16):
        print('{:04x}:'.format(i), end=" ")
        for j in bstr[i:i+16]:
            print("{:02x}".format(j), end=" ")
        print()

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


random_key = random_bytes()
random_key = b'a'*16
random_prefix = random_bytes(randint(0, 32))

b64encoded_plaintext = open('b64encoded_plaintext.txt').read()
p = base64.b64decode(b64encoded_plaintext)

def encryption_oracle(your_str):
    p_new = random_prefix + your_str + p
    k = random_key
    cipher = AES_ECB(k)
    c = cipher.encrypt(p_new)
    return c

def crack_ecb_harder(oracle):
    # discover BLKSIZE (+ plaintext size)
    plaintext_len = len(oracle(b''))
    BS = 0
    prefix_len = 0
    target_len = 0
    ori_pad_len = 0
    prefix_pad_len = 0
    prefix_padded_len = 0
    for i in range(1, plaintext_len):
        tmp_len = len(oracle(b'A'*i))
        if tmp_len > plaintext_len:
            BS = tmp_len - plaintext_len
            plaintext_len -= i
            break
    # detect prefix length
    for i in range(2*BS, 3*BS):
        tmp_c = oracle(b'A'*i)
        for j in range(0, plaintext_len - BS, BS):
            if tmp_c[j:j+BS] == tmp_c[j+BS:j+2*BS]:
                prefix_pad_len = (i - 2*BS)
                prefix_len = j - prefix_pad_len
                prefix_padded_len = j
                target_len = plaintext_len - prefix_len
                ori_pad_len = BS - target_len % BS
                break
        if ori_pad_len != 0:
            break

    # break: byte-at-a-time
    result = b''
    first_blk = b''
    sized_bytes = ori_pad_len
    padding_len = BS
    for _ in range(target_len):
        if padding_len > 1:
            padding_len -= 1
            sized_bytes += 1
            for i in range(256):
                tmp_blk = bytes([i]) + first_blk[0:BS-padding_len-1] + bytes([padding_len] * padding_len)
                tmp_blk += b'A' * sized_bytes
                c = oracle(b'A'*prefix_pad_len + tmp_blk)
                if c[prefix_padded_len:prefix_padded_len + BS] == c[-BS:]:
                    first_blk = tmp_blk[0:BS]
                    result = first_blk[:1] + result
                    break
            continue
        sized_bytes += 1
        sized_bytes = ((sized_bytes-ori_pad_len)%BS + ori_pad_len)
        for i in range(256):
            tmp_blk = bytes([i]) + first_blk[0:BS-1]
            tmp_blk += b'A' * sized_bytes
            c = oracle(b'A'*prefix_pad_len + tmp_blk)
            tmp = (len(result) - 15)//BS + 2
            if c[prefix_padded_len:prefix_padded_len + BS] == c[-tmp*BS:-tmp*BS+BS]:
                first_blk = tmp_blk[0:BS]
                result = first_blk[:1] + result
                break
    
    return result

def main():
    plaintext = crack_ecb_harder(encryption_oracle)
    # plaintext in bytes
    print_bytes(plaintext)
    # printed plaintext
    print(plaintext.decode())
        
if __name__ == "__main__":
    main()