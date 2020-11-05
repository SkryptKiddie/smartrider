# How to crack a smartrider  

## Prerequisites
- SmartRider
- USB NFC card reader
- mfoc
- libnfc_crypt1_crack
- SmartRider Sector 1 Key A

## Method 1 (older cards)
1. Connect the NFC card reader and with your card on the reader, run `mfoc -O dump.mfc`
2. MFOC should find the key for Sector 1 Key A and use that to decrypt the rest of the card.
3. If that works, mfoc will print the card contents in the terminal and into dump.mfc.
If MFOC says that the hardnested attack isn't supported, you must use the next method

## Method 2 (newer cards)
1. Connect the NFC reader and place your card on the reader.
2. Run `libnfc_crypto1_crack (key A) 0 A 0 B`, replacing (key A) with the key. Use method 1 to find the key (you can find the key, but mfoc can't crack the newer cards). __This will return your personal key A.__
3. If the key is found, run `libnfc_crypto1_crack FOUNDKEY 0 B 4 A`, replacing FOUNDKEY with the key that step 2 outputs. __This will return your personal key B.__
4. Once you have both keys, paste them both into a file called `keys.txt` in your working directory, on individual lines.
5. Run `mfoc -O dump.mfc -k keys.txt`.
6. Assuming all goes well, the terminal will output the card contents to the terminal and into dump.mfc.

## Example keys.txt
```
2031d1****** # universal key S1 KA
e23831****** # personal key A
c3922a****** # personal key B
```
