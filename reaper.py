#!/usr/bin/env python3

import os
import base64
import json

# Bundled
import dexed
import dx7

# Read reaper.rpp project file
with open(os.path.dirname(__file__) + '/reaper.rpp', 'r') as f:
    data = f.read()

lines = data.splitlines()

# Find all Dexed instances
dexed_vst3i_line_numbers = [i for i, line in enumerate(lines) if line.lstrip().startswith('<VST "VST3i: Dexed')]

# For each of those Dexed instances, get the intendation level (number of spaces before the '<VST "VST3i: Dexed' string)
for begin_line_number in dexed_vst3i_line_numbers:
    intendation_level = len(lines[begin_line_number]) - len(lines[begin_line_number].lstrip())
    print("Dexed instance begin line number: " + str(begin_line_number) + ", intendation level: " + str(intendation_level))
    end_line_number = None
    for i in range(begin_line_number + 1, len(lines)):
        if lines[i].startswith(' ' * intendation_level + '>'):
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
    print("Original dexed_state_dict:")
    print(json.dumps(dexed_state_dict, indent=4))

    # Edit dexed_state_dict here
    dexed_state_dict['dexedState']['@currentProgram'] = "0" # This does not actually change the loaded voice; to do that, change the ['dexedState']['dexedBlob']['@currentProgram']
    # dexed_state_dict['dexedState']['@opSwitch'] = "000001" # Only operator 1 is on; seems to change when another program is loaded from the Dexed UI
    # dexed_state_dict['dexedState']['@wheelMod'] = "7 1 1 1"
    # dexed_state_dict['dexedState']['@footMod'] = "8 1 1 1"
    # dexed_state_dict['dexedState']['@breathMod'] = "9 1 1 1"
    # dexed_state_dict['dexedState']['@aftertouchMod'] = "10 1 1 1"
    dexed_state_dict['dexedState']['@engineType'] = "0" # Modern
    
    # Edit the loaded bank of voices in dexed_state_dict
    sysex = dx7.make_init_vced32()
    sysex_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in sysex])
    dexed_state_dict['dexedState']['dexedBlob']['@sysex'] = sysex_hex

    # Edit the currently loaded voice in dexed_state_dict
    program = dx7.init_vced + [0x20, 0x00, 0x00, 0x00, 0x00, 0x00] # TODO: Document what these bytes mean
    program_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in program])
    dexed_state_dict['dexedState']['dexedBlob']['@program'] = program_hex

    # Encode dexed_state_dict back to XML
    dexed_state_xml = dexed.construct_dexed_xml(dexed_state_dict)
    # Replace dexed_state_xml inside decoded_blob2
    # Inside decoded_blob2, replace everything between the first '<' and the last '>' (including those) with dexed_state_xml
    decoded_blob2 = decoded_blob2[:decoded_blob2.find(b'<')] + dexed_state_xml.encode('ascii') + decoded_blob2[decoded_blob2.rfind(b'>')+1:]

    # Just for checking, decode the modified decoded_blob2 and print it
    print("Modified decoded blob 2:")
    dexed_state_dict = dexed.read_dexed_xml(decoded_blob2)
    print(json.dumps(dexed_state_dict, indent=4))

    # Encode the modified decoded_blob2 back to base64
    blob2 = base64.b64encode(decoded_blob2).decode('ascii')
    # Split into lines of 128 characters
    blob2_lines = [blob2[i:i+128] for i in range(0, len(blob2), 128)]
    # At the beginning of each line, add indentation_level + 2 spaces
    blob2_lines = [' ' * (intendation_level + 2) + line for line in blob2_lines]

    # Replace the lines for blob 2 with the modified blob 2 lines
    lines[begin_line_number + 2:end_line_number-1] = blob2_lines

    # From blob 3, get the preset name by removing everything before the first null byte, and removing everything after the second null byte
    preset_name = decoded_blob3.decode('ascii').split('\x00')[1].split('\x00')[0]
    print("Preset name from blob 3: " + preset_name)

# Write the modified project file
with open(os.path.dirname(__file__) + '/reaper_modified.rpp', 'w') as f:
    f.write('\n'.join(lines))
