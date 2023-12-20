#!/usr/bin/env python3

# Compare two rpp files

import dexed
import reaper
import base64

def main():
    file1 = 'reaper.rpp'
    file2 = 'reaper - Kopie.rpp'

    rpp1 = reaper.ReaperProject(file1)
    rpp1.read()

    rpp2 = reaper.ReaperProject(file2)
    rpp2.read()

    # Compare the lines
    for i in range(len(rpp1.lines)):
        # Strip the lines of whitespace
        rpp1.lines[i] = rpp1.lines[i].strip()
        rpp2.lines[i] = rpp2.lines[i].strip()
        if rpp1.lines[i] != rpp2.lines[i]:
            print("Line " + str(i) + " differs:")
            print("  " + rpp1.lines[i])
            print("  " + rpp2.lines[i])
            print()

    # Find all instances of Dexed
    PI1 = rpp1.find_plugin_instances('Dexed')
    PI2 = rpp2.find_plugin_instances('Dexed')


    # Compare blob0 to blob3 of the 2ns instance in the first rpp file with the first instance in the second rpp file
    for i in range(3):
        if PI1[1].raw_blobs[i] != PI2[1].raw_blobs[i]:
            print("Blob " + str(i) + " differs:")
            print("  " + PI1[1].raw_blobs[i])
            print("  " + PI2[1].raw_blobs[i])
            
            # Decode the blobs using base64
            decoded_blob1 = base64.b64decode(PI1[1].raw_blobs[i])
            decoded_blob2 = base64.b64decode(PI2[1].raw_blobs[i])
            if decoded_blob1 != decoded_blob2:
                print("Blob " + str(i) + " differs after decoding:")
                print("  " + str(decoded_blob1))
                print("  " + str(decoded_blob2))
                # Show the differences
                number_of_first_different_byte = None
                for j in range(len(decoded_blob1)):
                    if decoded_blob1[j] != decoded_blob2[j]:
                        print("Byte " + str(j) + " differs:")
                        print("  " + str(decoded_blob1[j]))
                        print("  " + str(decoded_blob2[j]))
                        number_of_first_different_byte = j
                        print()

                # From the first file, show 16 bytes around the first different byte, both in hex and ascii
                print("First file:")
                print("  " + str(decoded_blob1[number_of_first_different_byte-16:number_of_first_different_byte+16]))
                for j in range(number_of_first_different_byte-16, number_of_first_different_byte+16):
                    print("  " + str(decoded_blob1[j:j+1].hex().upper()), end='')

                print()
                # Now do the same for the second file
                print("Second file:")
                print("  " + str(decoded_blob2[number_of_first_different_byte-16:number_of_first_different_byte+16]))
                for j in range(number_of_first_different_byte-16, number_of_first_different_byte+16):
                    print("  " + str(decoded_blob2[j:j+1].hex().upper()), end='')
                print()



        else:
            print("Blob " + str(i) + " is identical.")
            print("This blob starts at line " + str(PI1[1].begin_line_number + i + 1) + " and ends at line " + str(PI1[1].end_line_number - 1) + ".")
            

if __name__ == '__main__':
    main()