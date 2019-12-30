# MT19937 Mersenne Twister RNG

* https://upload.wikimedia.org/wikipedia/commons/b/b5/Mersenne_Twister_visualisation.svg
* https://en.wikipedia.org/wiki/Mersenne_Twister
* https://www.guyrutenberg.com/2014/05/03/c-mt19937-example/
* http://www.cplusplus.com/reference/random/mt19937/
* w-bit word length, generates integers in the range $[0, 2^w - 1]$
* algorithm parameters
  * *w*: word size (in number of bits)
  * *n*: degree of recurrence
  * *m*: middle word, an offset used in the recurrence relation defining the series ***x***, 1 ≤ *m* < *n*
  * *r*: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ *r* ≤ *w* - 1
  * *a*: coefficients of the rational normal form twist matrix
  * *b*, *c*: TGFSR(R) tempering bitmasks
  * *s*, *t*: TGFSR(R) tempering bit shifts
  * *u*, *d*, *l*: additional Mersenne Twister tempering bit shifts/masks
* with the restriction that $2^{nw-r}-1$ is a Mersenne prime