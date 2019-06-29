import sys

def repeating_key_xor_enc(p, k):
    c = ""
    for i in range(len(p)):
        c += '{:02x}'.format(ord(p[i]) ^ ord(k[i % len(k)]))
    return c

def main():
    if (len(sys.argv) > 1):
        try:
            print('[+] Encrypting:\n {}'.format(sys.argv[1]))
            plain_text = open(sys.argv[1]).read()
            encrypted_text = repeating_key_xor_enc(plain_text, 'ICE')
            print('[+] Got result:\n', encrypted_text)
        except Exception as e:
            print('[x] Got error: ' + str(e))
        
    else:
        print('plz pass in the ori_text file path...')

if __name__ == "__main__":
    main()