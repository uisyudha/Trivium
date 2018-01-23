# Trivium
Implementation of Trivium Stream Cipher with Python

## Installation
Require bitstring 
```
pip install bitstring
```

## Usage
```
usage: trivium.py [-h] [-m {e,d}] [-k, --key KEY] [-iv IV] M

Decryption or encryption using Trivium stream cipher.

positional arguments:
  M                     Cipher text or plain text

optional arguments:
  -h, --help            show this help message and exit
  -m {e,d}, --mode {e,d}
                        Choose mode, e for encryption or d for decryption
  -k, --key KEY         An 80 bit key e.g.: 0x0000000000000000
  -iv IV                An 80 bit initialization vector e.g.:
                        0x0000000000000000

trivium.py -m e -k 0x80000000000000000000 -iv 0x00000000000000000000 ABCD
```