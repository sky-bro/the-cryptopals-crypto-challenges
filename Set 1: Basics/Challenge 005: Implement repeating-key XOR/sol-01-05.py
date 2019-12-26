#!/bin/python
import sys
import codecs


# same as dec actually
def repeating_key_xor_enc(p, k):
    return repeating_key_xor_dec(p, k)
    # c = []
    # for i in range(len(p)):
    #     c.append(p[i] ^ k[i % len(k)])
    # return bytes(c)


def repeating_key_xor_dec(c, k):
    p = []
    for i in range(len(c)):
        p.append(c[i] ^ k[i % len(k)])
    return bytes(p)


def main():
    if (len(sys.argv) > 1):
        try:
            print('[+] Encrypting:\n {}'.format(sys.argv[1]))
            plain_text = open(sys.argv[1]).read()
            key = b'ICE'

            encrypted_text = repeating_key_xor_enc(plain_text.encode(), key)
            print('[+] Got result:\n',
                  codecs.encode(encrypted_text, 'hex').decode())
            print('[+] Decrypting:\n')
            decrypted_text = repeating_key_xor_dec(
                encrypted_text, key)
            print('[+] Got back:\n', decrypted_text.decode())
        except Exception as e:
            print('[x] Got error: ' + str(e))

    else:
        print('plz pass in the ori_text file path...')


if __name__ == "__main__":
    main()
