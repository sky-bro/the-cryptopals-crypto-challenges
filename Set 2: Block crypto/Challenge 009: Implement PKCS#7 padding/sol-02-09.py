import sys


def pad(s, BS=16):
    needed_bytes_num = BS - len(s) % BS
    return s + bytes(needed_bytes_num*[needed_bytes_num])


def unpad(s):
    return s[:-s[-1]]


if __name__ == "__main__":
    padded = pad(b"YELLOW SUBMARINE", BS=20)
    print(padded)
    print(unpad(padded))
