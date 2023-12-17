#!/usr/bin/env python3

import os
import base64

import dexed
import json

# Read reaper.rpp project file
with open(os.path.dirname(__file__) + '/reaper.rpp', 'r') as f:
    data = f.read()

lines = data.splitlines()

# Find all Dexed instances
dexed_vst3i_line_numbers = [i for i, line in enumerate(lines) if line.lstrip().startswith('<VST "VST3i: Dexed')]

# For each of those Dexed instances, get the intendantion level (number of spaces before the '<VST "VST3i: Dexed' string)
for begin_line_number in dexed_vst3i_line_numbers:
    intendantion_level = len(lines[begin_line_number]) - len(lines[begin_line_number].lstrip())
    print("Dexed instance begin line number: " + str(begin_line_number) + ", intendantion level: " + str(intendantion_level))
    end_line_number = None
    for i in range(begin_line_number + 1, len(lines)):
        if lines[i].startswith(' ' * intendantion_level + '>'):
            end_line_number = i
    print("Dexed instance end line number: " + str(end_line_number))
    # Between the begin and end line numbers, there are 3 base64 encoded blobs. The fist and the last are one line each, the middle one is multiple lines.
    blob1 = lines[begin_line_number + 1].strip()
    blob2 = ''.join(lines[begin_line_number + 2:end_line_number-1]).strip().replace(' ', '')
    blob3 = lines[end_line_number-1].strip()
    print("Blob 1: " + blob1)
    print("Blob 2: " + blob2)
    print("Blob 3: " + blob3)
    # Decode the blobs using base64
    decoded_blob1 = base64.b64decode(blob1)
    decoded_blob2 = base64.b64decode(blob2)
    decoded_blob3 = base64.b64decode(blob3)
    # Print the decoded blobs
    print("Decoded blob 1 in hex: " + decoded_blob1.hex()) # Meaning unclear; does it contain the DX7 In and DX7 Out MIDI ports?
    print("Decoded blob 2:")
    dexed_state_dict = dexed.read_dexed_xml(decoded_blob2)
    print(json.dumps(dexed_state_dict, indent=4))

    # From blob 3, get the preset name by removing everything before the first null byte, and removing everything after the second null byte
    preset_name = decoded_blob3.decode('ascii').split('\x00')[1].split('\x00')[0]
    print("Preset name from blob 3: " + preset_name)