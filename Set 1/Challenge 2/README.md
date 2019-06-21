# Fixed XOR
> Write a function that takes two equal-length buffers and produces their XOR combination.

### If your function works properly, then when you feed it the string:

`1c0111001f010100061a024b53535009181c`

### ... after hex decoding, and when XOR'd against:

`686974207468652062756c6c277320657965`

### ... should produce:

`746865206b696420646f6e277420706c6179`

### Taking Notes

* [convert int to a hex str](https://stackoverflow.com/questions/2269827/how-to-convert-an-int-to-a-hex-string#2269836)
    * `'{:x}'.format(i)`
    * `chr, hex`
* [convert hex str to int](https://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python)
    * `int(string_1, 16)`