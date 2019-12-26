import sys


def has_valid_padding(s):  # s in bytes
    if not s:
        return False
    pad_len = s[-1]
    if pad_len > len(s):
        return False

    for i in range(len(s) - pad_len, len(s)):
        if s[i] != pad_len:
            return False
    return True


def strip_padding(s):
    return s[:-s[-1]]


def unpad(s):
    if not has_valid_padding(s):
        raise ValueError('wrong padding!')
    return strip_padding(s)


if __name__ == "__main__":
    s = b"ICE ICE BABY\x04\x04\x04\x04"
    # s = b"ICE ICE BABY\x05\x05\x05\x05"
    print(unpad(s).decode())
