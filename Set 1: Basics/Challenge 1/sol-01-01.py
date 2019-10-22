import sys
import codecs

def hex2base64(hex_str):
    plain_str = codecs.decode(hex_str, 'hex')
    print('[+] Plain text:\n', plain_str.decode())
    return codecs.encode(plain_str, 'base64').decode()

def main():
    if (len(sys.argv) > 1):
        try:
            base64_str = hex2base64(sys.argv[1])
            print('[+] Got base64_str:\n', base64_str)
        except Exception as e:
            print('[x] Hex2Base64 error: ' + str(e))
        
    else:
        print('plz pass in the hex_str for converting...')

if __name__ == "__main__":
    main()