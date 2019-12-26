import os
import json
import re
from Crypto.Cipher import AES
from random import randint

BS = 16

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

def parse_profile(profile_str):
    profile_dict = {}
    for i in profile_str.split('&'):
        i = i.split('=')
        profile_dict[i[0]] = i[1]
    return json.dumps(profile_dict)

# uid = 1
def profile_for(email):
    '''
    given foo@bar.com, produce email=foo@bar.com&uid=10&role=user
    should not allow encoding metacharacters (& and =) -- eat them, quote them, whatever
    don't let people set email to foo@bar.com&role=admin
    '''
    # global uid
    # should not be so rigorous? unable to construct email with padding character (ascii code: 1~BS)
    # if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
    #      email):
    #      return
    profile_str = "email={}&uid={}&role=user".format(email, 10)
    # uid += 1
    return profile_str

# generate random key
key = os.urandom(16)
cipher = AES_ECB(key)

def enc_profile(profile_str):
    return cipher.encrypt(profile_str)

def dec_profile(crypted_profile):
    return cipher.decrypt(crypted_profile)

def get_each_blk(blks, BS=16):
    for i in range(0, len(blks), BS):
        tmp = blks[i:i+BS]
        yield tmp

def adversary():
    '''
+++ email=xxxx@xxxx.
--- admin00000000000
+++ xxx&uid=10&role=
--- user000000000000
+++ admin00000000000
    '''
    pad_len = BS - len(b'admin')
    email = b'a'*(BS - 3 - 6) + b'@a.'
    email += b'admin' + bytes([pad_len] * pad_len)
    email += b'a' * (BS - 13)
    print("Try Email:", email)

    c0 = profile_for(email.decode())
    c0 = enc_profile(c0.encode())
    print("\nGot ciphertext:")
    list(map(print, get_each_blk(c0, BS)))

    crypted_profile = c0[0:BS] + c0[2*BS:3*BS] + c0[BS:2*BS]
    print('\nConstructed Crypted_profile:')
    list(map(print, get_each_blk(crypted_profile, BS)))

    # email=input('Email: ')
    # while email:
        
    #     profile_str = profile_for(email)
    #     print('profile:', profile_str)
    #     print('profile len: {} + {} = {}'.format(len(email), 23, len(profile_str)))
    #     crypted_profile = enc_profile(profile_str.encode())
    #     print("crypted:\nlen: {}\n{}".format(len(crypted_profile), list(crypted_profile)))
    #     email = input('Next Email: ')
        
    return crypted_profile

def main():
    crypted_profile = adversary()
    profile_str = dec_profile(crypted_profile).decode()
    print("\nConstructed Profile")
    print(profile_str)
    profile_json = parse_profile(profile_str)
    print(profile_json)
        
if __name__ == "__main__":
    main()