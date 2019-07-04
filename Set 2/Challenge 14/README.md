# Byte-at-a-time ECB decryption (Harder)

### Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:
```
AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
```

### Same goal: decrypt the target-bytes.

### Stop and think for a second.

* What's harder than challenge #12 about doing this? How would you overcome that obstacle? The hint is: you're using all the tools you already have; no crazy math is required.

* Think "STIMULUS" and "RESPONSE".

### notes

* take notice that here the random-prefix is first generated and then fixed for every new encryption process!
* the key is just to get the length of that random-prefix, which is quite easy!
    * we increase the length of our controled str once at a time with the same chr
    * first time we see a jump in the block_cnt, we known len(prefix) + len(target)
    * keep increasing...
    * when we first see two contiguous & identical blk, we known the length of our prefix!