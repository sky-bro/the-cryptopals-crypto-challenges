// operators in c c++: 'and' is not bitwise, but xor is, bitwise and, or: 'bitand', 'bitor'
// https://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B
#include <iostream>
#include <random>

using namespace std;

/* 
(w, n, m, r) = (32, 624, 397, 31)
a = 9908B0DF16
(u, d) = (11, FFFFFFFF16)
(s, b) = (7, 9D2C568016)
(t, c) = (15, EFC6000016)
l = 18
 */
// w = 32， 那这里直接用int就合适
const unsigned w = 32, n = 624, m = 397, r = 31;
const unsigned a = 0x9908B0DF;
const unsigned u = 11, d = 0xFFFFFFFF;
const unsigned s = 7, b = 0x9D2C5680;
const unsigned t = 15, c = 0xEFC60000;
const unsigned l = 18, f = 0x6C078965; // 32-bit的f为1812433253，64-bit的为6364136223846793005

// Create a length n array to store the state of the generator
unsigned MT[n];
unsigned index = n + 1;
const unsigned lower_mask = (1 << r) - 1; // That is, the binary number of r 1's
const unsigned upper_mask = ~lower_mask;

// Initialize the generator from a seed
void seed_mt(int seed) {
    MT[0] = seed;
    for (int i = 1; i < n; ++i) { // loop over each element
        MT[i] = f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i;
    }
    index = n;
}

// Generate the next n values from the series x_i 
void twist() {
    for (int i = 0; i < n; ++i) {
        unsigned x = (MT[i] & upper_mask)
                + (MT[(i+1) % n] & lower_mask);
        unsigned xA = x >> 1;
        if ((x % 2) != 0) { // lowest bit of x is 1
            xA = xA ^ a;
        }
        MT[i] = MT[(i + m) % n] ^ xA;
    }
    index = 0;
}

// Extract a tempered value based on MT[index]
// calling twist() every n numbers
unsigned extract_number() {
    if (index >= n) {
        if (index > n) {
            printf("Generator was never seeded");
            return -1;
            // Alternatively, seed with constant value; 5489 is used in reference C code[48]
        }
        twist();
    }

    unsigned y = MT[index];
    y = y ^ ((y >> u) & d);
    y = y ^ ((y << s) & b);
    y = y ^ ((y << t) & c);
    y = y ^ (y >> l);

    index += 1;
    return y;
}

int main(int argc, char const *argv[])
{
    time_t seed = time(0);
    // seed = 0;
    seed_mt(seed);
    mt19937 mt_rand(seed);

    for (int i = 0; i < n*2; ++i) {
        unsigned output = extract_number();
        unsigned output2 = mt_rand();
        cout<<"output "<<i<<": "<<output<<endl;
        if (output != output2) {
            cout<<"Got you: "<<i<<endl;
            cout<<"output2: "<<output2<<endl;
            break;
        }
    }
    return 0;
}
