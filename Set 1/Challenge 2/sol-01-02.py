import sys

def bytes_xor(bytes_a, bytes_b):
    result = []
    for i in range(min(len(bytes_a), len(bytes_b))):
        result.append(bytes_a[i] ^ bytes_b[i])
    return bytes(result)

def fixedXor(a, b):
    a = bytes.fromhex(a)
    b = bytes.fromhex(b)
    return bytes_xor(a, b).hex()

def main():
    if (len(sys.argv) > 2):
        xor_result = fixedXor(sys.argv[1], sys.argv[2])
        print('[+] Xoring:\n {}\n {}'.format(sys.argv[1], sys.argv[2]))
        print('[+] Got result:\n', xor_result)
        
    else:
        print('plz pass in two hex_str for XOR...')

if __name__ == "__main__":
    main()