import sys

def detect_ecb_mode(c, blk_size = 32):
    blks = [c[i:i+blk_size] for i in range(0, len(c), blk_size)]
    distinct_blk_rate = len(set(blks))/len(blks)
    return distinct_blk_rate

def main():
    if (len(sys.argv) < 2):
        print('Please pass in file path...')
        return -1
    f = open(sys.argv[1])
    i = 0
    rates_arr = []
    for line in f.readlines():
        i += 1
        rates_arr.append((i, detect_ecb_mode(line)))
    rates_arr.sort(key=lambda x: x[1])
    print(rates_arr)

if __name__ == "__main__":
    main()