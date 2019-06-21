import sys
import codecs

def singleByteXorCipher_decrypt(c):
    print(len(c))
    def keyTest(c, k):
        plain_text = ''
        for i in range(0, len(c), 2):
            plain_text += '{:02x}'.format(int(c[i:i+2], 16) ^ k)
        return codecs.decode(plain_text.encode(), 'hex').decode()
    
    def frequencyScore(english_text):
        # check letter frequency of E:12.02, T:9.10, A:8.12
        return 1

    result = ''
    confidence = 0
    for k in range(128):
        tmp_result = keyTest(c, k)
        tmp_confidence = frequencyScore(tmp_result)
        print('key{}'.format(k), tmp_result)
        if tmp_confidence > confidence:
            result = tmp_result

    return (result, confidence)

def main():
    if (len(sys.argv) > 1):
        try:
            plain_text = singleByteXorCipher_decrypt(sys.argv[1])
            print('[+] Decrypting:\n {}'.format(sys.argv[1]))
            print('[+] Got result:\n', plain_text)
        except Exception as e:
            print('[x] fixedXor error: ' + str(e))
        
    else:
        print('plz pass in the cipher text(hex encoded str xor\'d by a single character)...')

if __name__ == "__main__":
    main()