import sys

def pad(s, BS=16):
    needed_bytes_num = BS - len(s) % BS
    return s + needed_bytes_num * chr(needed_bytes_num)

def unpad(s):
    return s[:-ord(s[-1])]

# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
# unpad = lambda s : s[:-ord(s[len(s)-1:])]

# def main():
#     pass

# if __name__ == "__main__":
#     main()