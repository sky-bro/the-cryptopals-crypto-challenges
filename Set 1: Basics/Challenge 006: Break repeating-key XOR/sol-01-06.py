import sys
import base64
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
        elif ch in '\':,.!-0123456789 \r\t\n':
            ignored += 1
        else:
            # print(ch)
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
    for i in range(len(c)):
        plain_text += '{:02x}'.format(c[i] ^ k)
    try:
        return codecs.decode(plain_text.encode(), 'hex').decode()
    except Exception as e:
        raise Exception(e)

def single_byte_xor(c):
    # print('length of c', len(c))
    result = ''
    closeness = -1
    ch = ''
    for k in range(256):
        # tmp_result = keyTest(c, k)
        # tmp_closeness = dist2eng(tmp_result)
        # if (tmp_closeness != -1 and tmp_closeness < closeness) or closeness == -1:
        #     result = tmp_result
        #     closeness = tmp_closeness
        try:
            tmp_result = keyTest(c, k)
            tmp_closeness = dist2eng(tmp_result)
            if (tmp_closeness != -1 and tmp_closeness < closeness) or closeness == -1:
                result = tmp_result
                closeness = tmp_closeness
                ch = chr(k)
        except Exception:
            pass
    return (result, closeness, ch)

def diff_bits(a, b):
    ret = 0
    for i in range(len(a)):
        ori = a[i] ^ b[i]
        while ori != 0:
            ret += 1 if ori & 1 else 0
            ori = ori >> 1
    return ret

# def test_key_size(, key_len)

def brk_repeating_key_xor(c):
    avg_diff_bits_arr = []
    likely_key_len = len(c)
    # at least has two blks
    for key_len in range(2, min(41, len(c)//2)):
        tmp_avg_diff_bits = 0
        
        for blk_i in range(len(c)//key_len - 1):
            begin = blk_i * key_len
            tmp_avg_diff_bits += diff_bits(c[begin:begin+key_len], c[begin+key_len: begin+2*key_len])
        tmp_avg_diff_bits /= ((len(c)//key_len - 1)*key_len)
        # every key_len character has tmp_avg_diff_bits are different
        print(tmp_avg_diff_bits, key_len)
        avg_diff_bits_arr.append((tmp_avg_diff_bits, key_len))
    avg_diff_bits_arr.sort(key=lambda x: x[0])
    print(avg_diff_bits_arr)

    result = []
    # the most likely key_len has the smallest number of diff_bits
    likely_key_len = avg_diff_bits_arr[0][1]
    for i in range(likely_key_len):
        result.append(single_byte_xor(c[i::likely_key_len]))
    print(''.join(map(lambda x: x[2], result)))



def main():
    if len(sys.argv) < 2:
        print("please pass in the file path to break repeating-key xor...")
        return
    f = open(sys.argv[1])
    code = f.read()
    code = base64.b64decode(code.encode())
    # print(code)
    # print(diff_bits('this is a test'.encode(), 'wokka wokka!!!'.encode()))
    brk_repeating_key_xor(code)

if __name__ == "__main__":
    main()