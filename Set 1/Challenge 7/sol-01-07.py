import sys
import base64
from Crypto.Cipher import AES

# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def main():
    if len(sys.argv) < 2:
        print('Please pass the file path...')
        return -1
    f = open(sys.argv[1])
    c = base64.b64decode(f.read())
    aes_ecb = AES.new('YELLOW SUBMARINE')
    text = aes_ecb.decrypt(c).decode()
    text = unpad(text)
    print(text)

if __name__ == "__main__":
    main()