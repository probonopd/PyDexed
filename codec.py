#!/usr/bin/env python3

# This script implements the non-standard JUCE implementation of Base64 encoding/decoding
# https://github.com/juce-framework/JUCE/blob/master/modules/juce_core/memory/juce_MemoryBlock.cpp#L353C1-L411C2

encodingTable = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+"

def _setBitRange(size, data, bitRangeStart, numBits, bitsToSet):
    bite = bitRangeStart >> 3
    offsetInByte = int(bitRangeStart & 7)
    mask = ~(((0xffffffff) << (32 - numBits)) >> (32 - numBits))
    while numBits > 0 and bite < size:
        bitsThisTime = min(numBits, 8 - offsetInByte)
        tempMask = (mask << offsetInByte) | ~(((0xffffffff) >> offsetInByte) << offsetInByte)
        tempBits = bitsToSet << offsetInByte
        data[bite] = (data[bite] & tempMask) | tempBits
        bite += 1
        numBits -= bitsThisTime
        bitsToSet >>= bitsThisTime
        mask >>= bitsThisTime
        offsetInByte = 0

def fromJuceBase64Encoding(s):
    """
    Decodes a string encoded in JUCE Base64 format.

    Args:
        s (str): The JUCE Base64 encoded string.

    Returns:
        bytes: The decoded data.

    """
    size = int(s[:s.index(".")])
    b64str = s[s.index(".") + 1:]
    pos = 0
    data = [0] * size
    for i in range(len(b64str)):
        c = b64str[i]
        for j in range(64):
            if encodingTable[j] == c:
                _setBitRange(size, data, pos, 6, j)
                pos += 6
                break
    return bytes(i & 0xff for i in data)

def _getBitRange(size, data, bitRangeStart, numBits):
    res = 0
    byte = bitRangeStart >> 3
    offsetInByte = bitRangeStart & 7
    bitsSoFar = 0
    while numBits > 0 and byte < size:
        bitsThisTime = min(numBits, 8 - offsetInByte)
        mask = (0xff >> (8 - bitsThisTime)) << offsetInByte
        res |= (((data[byte] & mask) >> offsetInByte) << bitsSoFar)
        bitsSoFar += bitsThisTime
        numBits -= bitsThisTime
        byte += 1
        offsetInByte = 0
    return res

def toJuceBase64Encoding(bytes):
    """
    Converts a byte array to JUCE Base64 encoding.

    Args:
        bytes (bytes): The byte array to be encoded.

    Returns:
        str: The JUCE Base64 encoded string.
    """
    if not bytes:
        return None
    numChars = ((len(bytes) << 3) + 5) // 6
    s = str(len(bytes)) + '.'
    for i in range(numChars):
        s += encodingTable[_getBitRange(len(bytes), bytes, i * 6, 6)]
    return s

def main():
    # Read Dexed_01.syx file and convert to base64 using the above functions
    with open('Dexed_01.syx', 'rb') as file:
        data = file.read()
    base64_encoding = toJuceBase64Encoding(data)
    # print(base64_encoding)

    # The result is identical to what we have in the savedstate.dexed file
    # Read savestate.dexed file into a string
    with open('savedstate.dexed', 'r') as file:
        data = file.read()

    # Find the first occurence of "base64:sysex=", and find the position of the next two '"' characters after that.
    # The string between those two '"' characters is the base64 encoded data.
    pos = data.find("base64:sysex=")
    pos1 = data.find('"', pos + 13)
    pos2 = data.find('"', pos1 + 1)
    base64_from_dexed = data[pos1 + 1:pos2]

    # print(base64_from_dexed)

    # Compare the two base64 encoded data strings and print whether they are identical
    print("The two base64 encoded data strings are identical: " + str(base64_encoding == base64_from_dexed))

if __name__ == "__main__":
    main()