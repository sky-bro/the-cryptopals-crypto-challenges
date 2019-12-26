#!/bin/python3
import os
import sys
import base64
import string
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
# random_key = b'a'*16

b64encoded_plaintext = open('b64encoded_plaintext.txt').read()
p = base64.b64decode(b64encoded_plaintext)


def encryption_oracle(your_str, BS=16):
    p_new = your_str + p
    k = random_key
    cipher = AES_ECB(k, BS)
    c = cipher.encrypt(p_new)
    return c


def crack_ecb(oracle, BS=16):
    # discover BLKSIZE (+ plaintext size)
    plaintext_len = len(oracle(b'', BS))
    BS = plaintext_len
    ori_pad_len = 0
    # i为前缀（用户可控制部分）长度
    # padding len: [1, BS]
    # BS: [1, plaintext_len], 当BS等于plaintext表示原文长度为0
    # 不断增加原文长度，直到密文长度变化（增加），增加的长度即为块长BS
    for i in range(1, plaintext_len+1):
        tmp_len = len(oracle(b'A'*i, BS))
        # 逐渐前缀长度到刚好需要额外pad一个BS
        if tmp_len > plaintext_len:
            # 密文增加的长度便是BS
            BS = tmp_len - plaintext_len
            # 待解的未知明文的长度就是原始密文长度-i
            plaintext_len -= i
            # 原来的pad长度是i
            ori_pad_len = i
            break
    # print(BS, plaintext_len)

    # detect indeed using ECB (repeated cipher blk)
    tmp_c = oracle(b'A'*BS*2, BS)
    if tmp_c[0:BS] == tmp_c[BS:2*BS]:
        print("ECB mode detected!")
    else:
        print("ECB mode not detected!\nBye!")
        exit()

    # break: byte-at-a-time
    result = b''
    first_blk = b''
    sized_bytes = ori_pad_len
    padding_len = BS
    # 每次求出一个byte，一共plaintext_len个byte需要求，每次将
    for _ in range(plaintext_len):
        sized_bytes += 1
        # padding_len 从BS到2，即首先破解出B-1个字节
        if padding_len > 1:
            padding_len -= 1
            for i in string.printable.encode():
            # for i in range(256):
                # 从后往前爆破
                tmp_blk = bytes([i]) + first_blk[0:BS-padding_len-1] + \
                    bytes([padding_len] * padding_len)
                tmp_blk += b'A' * sized_bytes
                c = oracle(tmp_blk, BS)
                if c[0:BS] == c[-BS:]:
                    first_blk = tmp_blk[0:BS]
                    result = first_blk[:1] + result
                    break
            continue
        sized_bytes = ((sized_bytes-ori_pad_len) % BS + ori_pad_len)
        for i in string.printable.encode():
        # for i in range(256):
            tmp_blk = bytes([i]) + first_blk[0:BS-1]
            tmp_blk += b'A' * sized_bytes
            c = oracle(tmp_blk, BS)
            tmp = (len(result) - (BS-1))//BS + 2
            if c[0:BS] == c[-tmp*BS:-tmp*BS+BS]:
                first_blk = tmp_blk[0:BS]
                result = first_blk[:1] + result
                break

    return result


def main():
    plaintext = crack_ecb(encryption_oracle, BS=32)
    # plaintext in bytes
    print_bytes(plaintext)
    # printed plaintext
    print(plaintext.decode())


if __name__ == "__main__":
    main()
