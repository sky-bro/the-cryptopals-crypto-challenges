# Single-byte XOR cipher

### The hex encoded string:

`1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736`

### ... has been XOR'd against a single character. Find the key, decrypt the message.

> You can do this by hand. But don't: write code to do it for you.
How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

### Achievement Unlocked
You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.

### Answer
key: 'X'
plaintext: Cooking MC's like a pound of bacon

### Taking Notes

* [English Letter Frequency (based on a sample of 40,000 words)](http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html)
* [Frequency Analysis](https://crypto.interactive-maths.com/frequency-analysis-breaking-the-code.html)
* Approximate Measurement
    * [Bhattacharyya distance](https://en.wikipedia.org/wiki/Bhattacharyya_distance#Bhattacharyya_coefficient)
* [Developing algorithm for detecting plain text via frequency analysis
](https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis)