# Require bitstring package
# pip install bitstring
from collections import deque
from itertools import repeat
from bitstring import BitArray

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

        
        self.state.rotate(1)

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
        # Enkripsi msg dengan keystream
        pass

    def decrypt(self, cipher):
        # Dekripsi
        pass

def main():
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

    
if __name__ == "__main__":
    main()

