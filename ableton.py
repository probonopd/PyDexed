#!/usr/bin/env python3

# Read Ableton .als or Instrument Rack .adg file and extract Dexed VST3 state

import binascii
import xml.etree.ElementTree as ET
import sys
import gzip
import os

import dexed
import dx7

def main(filename):
    # Read the XML content from the file
    try:
        if filename.endswith('.adg') or filename.endswith('.als'):
            with gzip.open(filename, 'rt') as file:
                xml_content = file.read()
        else:
            with open(filename, 'r') as file:
                xml_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    # Parse the XML content
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        sys.exit(1)

    # Find each ProcessorState tag and decode and parse its content
    i = 0
    for processor_state_tag in root.findall('.//ProcessorState'):
        if processor_state_tag is None or processor_state_tag.text is None:
            print("Error: No ProcessorState tag found or it is empty.")
            sys.exit(1)

        # Clean up the text content
        processor_state_hex = ''.join(processor_state_tag.text.split())

        # Decode the hexadecimal string
        try:
            decoded_bytes = binascii.unhexlify(processor_state_hex)
        except binascii.Error as e:
            print(f"Error decoding hex string: {e}")
            sys.exit(1)

        # Skip if "dexedState" is not found in the decoded bytes
        if b"dexedState" not in decoded_bytes:
            continue

        # Parse the Dexed VST3 state
        try:
            DS = dexed.DexedState()
            DS.parse_data_blob(decoded_bytes)
        except Exception as e:
            print(f"Error parsing Dexed VST3 state: {e}")
            sys.exit(1)

        # Pretty print the Dexed VST3 state
        print("Dexed VST3 state number " + str(i) + ":")
        # print(DS)
        i += 1

        # From the DS, get the program and from that the voice name
        program_hex = DS.dexed_state_dict['dexedState']['dexedBlob']['@program']
        program_bytes = binascii.unhexlify(program_hex.replace(" ", ""))
        voice_name = dx7.get_voice_name(program_bytes)
        print("Voice name: " + voice_name)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: " + os.path.basename(__file__) + " <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
