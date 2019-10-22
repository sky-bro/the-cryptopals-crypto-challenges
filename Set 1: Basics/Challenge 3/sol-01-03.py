import sys
import codecs

freq_exp = {
    'e': .1202, 't': .0910, 'a': .0812, 'o': .0768, 
    'i': .0731, 'n': .0695, 's': .0628, 'r': .0602, 
    'h': .0592, 'd': .0432, 'l': .0398, 'u': .0288, 
    'c': .0271, 'm': .0261, 'f': .0230, 'y': .0211, 
    'w': .0209, 'g': .0203, 'p': .0182, 'b': .0149, 
    'v': .0111, 'k': .0069, 'x': .0017, 'q': .0011, 
    'j': .0010, 'z': .0007
}

def dist2eng(english_text):
    count = {}
    ignored = 0
    for i in range(26):
        count[i] = 0
    for ch in english_text:
        c = ord(ch)
        if c >= 0x41 and c <= 0x5a:
            count[c - 0x41] += 1
        elif c >= 0x61 and c <= 0x7a:
            count[c - 0x61] += 1
        elif ch in '\' \n':
            ignored += 1
        else:
            return -1
    chi2 = 0
    letter_len = len(english_text) - ignored
    for i in range(26):
        observed = count[i]
        expected = letter_len * freq_exp[chr(i + 0x61)]
        difference = observed - expected
        chi2 += difference**2/expected
    return chi2

def keyTest(c, k):
    plain_text = ''
    for i in range(0, len(c), 2):
        plain_text += '{:02x}'.format(int(c[i:i+2], 16) ^ k)
    try:
        return codecs.decode(plain_text.encode(), 'hex').decode()
    except Exception as e:
        raise Exception(e)

def single_byte_xor(c):
    # print('length of c', len(c))
    result = ''
    closeness = -1
    for _ in range(256):
        try:
            tmp_result = keyTest(c, 53)
            tmp_closeness = dist2eng(tmp_result)
            if (tmp_closeness != -1 and tmp_closeness < closeness) or closeness == -1:
                result = tmp_result
                closeness = tmp_closeness
        except Exception:
            pass
        # print('key{}'.format(k), tmp_result, tmp_closeness)
    return (result, closeness)

def main():
    if (len(sys.argv) > 1):
        try:
            print('[+] Decrypting:\n {}'.format(sys.argv[1]))
            plain_text = single_byte_xor(sys.argv[1])
            print('[+] Got result:\n', plain_text)
        except Exception as e:
            print('[x] fixedXor error: ' + str(e))
        
    else:
        print('plz pass in the cipher text(hex encoded str xor\'d by a single character)...')

if __name__ == "__main__":
    main()