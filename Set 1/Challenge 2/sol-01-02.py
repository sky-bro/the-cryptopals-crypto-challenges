import sys

def fixedXor(a, b):
    def hex2Int(h):
        # h = h.lower()
        # a = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')
        # return a.index(h)
        return int(h, 16)

    def int2Hex(i):
        return '{:x}'.format(i)

    result = ''
    for i in range(min(len(a), len(b))):
        result += int2Hex(hex2Int(a[i]) ^ hex2Int(b[i]))
    return result

def main():
    if (len(sys.argv) > 2):
        try:
            xor_result = fixedXor(sys.argv[1], sys.argv[2])
            print('[+] Xoring:\n {}\n {}'.format(sys.argv[1], sys.argv[2]))
            print('[+] Got result:\n', xor_result)
        except Exception as e:
            print('[x] fixedXor error: ' + str(e))
        
    else:
        print('plz pass in two hex_str for XOR...')

if __name__ == "__main__":
    main()