# Require bitstring package
# pip install bitstring
from collections import deque
from itertools import repeat
from bitstring import BitArray
import argparse

class Trivium:
    def __init__(self, key, iv):
        self.state = None
        self.key = key
        self.iv = iv

        # Initialize state
        # (s1; s2; : : : ; s93) (K1; : : : ; K80; 0; : : : ; 0)
        init_state = self.key
        init_state += list(repeat(0, 13))

        #(s94; s95; : : : ; s177) (IV1; : : : ; IV80; 0; : : : ; 0)
        init_state += self.iv
        init_state += list(repeat(0, 4))

        #(s178; s279; : : : ; s288) (0; : : : ; 0; 1; 1; 1)
        init_state += list(repeat(0, 108))
        init_state += [1,1,1]

        self.state = deque(init_state)

        # Do 4 Full cycle clock
        for i in range(4*288):
            self.gen_keystream()

    def gen_keystream(self):
        t_1 = self.state[65] ^ self.state[92]
        t_2 = self.state[161] ^ self.state[176]
        t_3 = self.state[242] ^ self.state[287]

        z = t_1 ^ t_2 ^ t_3

        t_1 = t_1 ^ self.state[90] & self.state[91] ^ self.state[170]
        t_2 = t_2 ^ self.state[174] & self.state[175] ^ self.state[263]
        t_3 = t_3 ^ self.state[285] & self.state[286] ^ self.state[68]

        
        self.state.rotate()

        self.state[0] = t_3
        self.state[93] = t_1
        self.state[177] = t_2

        return z

    def keystream(self, msglen):
        # Generete keystream
        counter = 0
        keystream = []

        while counter < msglen:
            keystream.append(self.gen_keystream())
            counter += 1

        return keystream
        
    
    def encrypt(self, msg):
        all_chiper = []

        for i in range(len(msg)):
            hex_plain = hex(ord(msg[i]))
            
            keystream = self.keystream(8)
            keystream = '0b' + ''.join(str(i) for i in keystream[::-1])
            keystream = BitArray(keystream)
            keystream.byteswap()
            
            plain = BitArray(hex_plain)
            plain.byteswap()

            cipher = [x ^ y for x, y in zip(map(int, list(plain)), map(int, list(keystream)))]
            all_chiper += cipher

            cipher = '0b' + ''.join(str(i) for i in cipher)
            cipher = BitArray(cipher)
            cipher.byteswap()

            print '{: ^15}{: ^15}{: ^15}{: ^15}{:^15}'.format(hex_plain, plain.bin, keystream.bin, cipher.bin, '0x' + cipher.hex.upper())

        return all_chiper

    def decrypt(self, cipher):
        # Dekripsi
        pass

def main():
    """
    KEY = BitArray("0x80000000000000000000")
    print "Key : ", KEY.hex
    KEY.byteswap()
    KEY = map(int, KEY.bin)

    IV = BitArray("0x00000000000000000000")
    print "IV : ", IV.hex
    IV.byteswap()
    IV = map(int, IV.bin)

    trivium = Trivium(KEY, IV)
    keystream = trivium.keystream(128)

    hex_keystream = '0b' + ''.join(str(i) for i in keystream[::-1])
    hex_keystream = BitArray(hex_keystream)
    hex_keystream.byteswap()
    print "Keystream : ", hex_keystream.hex.upper()
    """
    parser = argparse.ArgumentParser(description='Decryption or encryption using Trivium stream cipher.',
        epilog="trivium.py -m e -k 0x80000000000000000000 -iv 0x00000000000000000000 ABCD")
    parser.add_argument('-m', '--mode', type=str, choices=['e', 'd'],
        help='Choose mode, e for encryption or d for decryption')
    parser.add_argument('-k, --key', action='store', dest='key', type=str,
        help='An 80 bit key e.g.: 0x0000000000000000')
    parser.add_argument('-iv', action='store', dest='iv', type=str,
        help='An 80 bit initialization vector e.g.: 0x0000000000000000')
    parser.add_argument('M', help='Cipher text or plain text')

    args = parser.parse_args()
    
    # Initialize Trivium
    KEY = BitArray(args.key)
    print '{:<15}{:<2}{:<10}'.format('KEY', '=', KEY.hex)
    KEY.byteswap()
    KEY = map(int, KEY.bin)

    IV = BitArray(args.iv)
    print '{:<15}{:<2}{:<10}'.format('IV', '=', IV.hex)
    IV.byteswap()
    IV = map(int, IV.bin)

    trivium = Trivium(KEY, IV)

    # Encryption mode
    if args.mode == 'e':
        print '{:<15}{:<2}{:<10}\n'.format('PLAIN TEXT', '=', args.M)
        print '{: ^15}{: ^15}{: ^15}{: ^15}{: ^15}'.format('INPUT', 'PLAIN TEXT', 'KEYSTREAM', 'CIPHER TEXT', 'OUTPUT')
        print '{:->75}'.format(' ')
        
        cipher = trivium.encrypt(args.M)
        cipher = '0b' + ''.join(str(i) for i in cipher)
        cipher = BitArray(cipher)
    else:
        print '{:<15}{:<2}{:<10}\n'.format('CIPHER TEXT', '=', args.M)
        print '{: ^15}{: ^15}{: ^15}{: ^15}{: ^15}'.format('INPUT', 'CIPHER TEXT', 'KEYSTREAM', 'PLAIN TEXT', 'OUTPUT')
        print '{:->75}'.format(' ')
        print 'Not yet implemented'
        pass
    
if __name__ == "__main__":
    main()

