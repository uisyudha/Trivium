from trivium import Trivium
from bitstring import BitArray

def main():
    print "Test vectors -- set 1"
    print "====================="
    
    KEY = BitArray("0x80000000000000000000")
    print "Key : ", KEY.hex
    KEY.byteswap()
    KEY = map(int, KEY.bin)

    IV = BitArray("0x00000000000000000000")
    print "IV : ", IV.hex
    IV.byteswap()
    IV = map(int, IV.bin)

    trivium = Trivium(KEY, IV)
    generete_keystream = trivium.keystream(128)
    
    hex_keystream = '0b' + ''.join(str(i) for i in generete_keystream[::-1])
    hex_keystream = BitArray(hex_keystream)
    hex_keystream.byteswap()
    print "Keystream : ", hex_keystream.hex.upper()

    assert hex_keystream.hex.upper() == '38EB86FF730D7A9CAF8DF13A4420540D'
    print "OK"

    
if __name__ == "__main__":
    main()