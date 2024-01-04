#!/usr/bin/env python3

import os
import base64
import json

# Bundled
import dexed
import dx7

class PluginInstance:
    def __init__(self, lines, begin_line_number):
        self.lines = lines
        self.begin_line_number = begin_line_number

        self.intendation_level = len(self.lines[begin_line_number]) - len(self.lines[begin_line_number].lstrip())
        # print("Dexed instance begin line number: " + str(begin_line_number) + ", intendation level: " + str(self.intendation_level))
        self.end_line_number = None
        for i in range(begin_line_number + 1, len(self.lines)):
            if self.lines[i].startswith(' ' * self.intendation_level + '>'):
                self.end_line_number = i
                break
        # print("Dexed instance end line number: " + str(self.end_line_number))

        # Between the begin and end line numbers, there are 3 base64 encoded blobs. The fist and the last are one line each, the middle one is multiple lines.
        blob0 = self.lines[self.begin_line_number + 1].strip()
        blob1 = ''.join(self.lines[self.begin_line_number + 2:self.end_line_number-1]).strip().replace(' ', '')
        blob2 = self.lines[self.end_line_number-1].strip()

        self.raw_blobs = [blob0, blob1, blob2]

        # Add padding to the blobs so that they are a multiple of 4 bytes long
        blob0 += '=' * (4 - len(blob0) % 4)
        blob1 += '=' * (4 - len(blob1) % 4)
        blob2 += '=' * (4 - len(blob2) % 4)

        # Decode the blobs using base64
        decoded_blob0 = base64.b64decode(blob0)
        decoded_blob1 = base64.b64decode(blob1)
        decoded_blob2 = base64.b64decode(blob2)

        self.blobs = [decoded_blob0, decoded_blob1, decoded_blob2]

    def update_blob(self, blob_number, new_blob):
        # Encode the modified blob back to base64
        new_blob = base64.b64encode(new_blob).decode('ascii')
        # Split into lines of 128 characters
        blob_lines = [new_blob[i:i+128] for i in range(0, len(new_blob), 128)]
        # At the beginning of each line, add indentation_level + 2 spaces
        blob_lines = [' ' * (self.intendation_level + 2) + line for line in blob_lines]

        # Replace the lines for the blob with the modified blob lines
        self.lines[self.begin_line_number + blob_number + 1:self.end_line_number-1] = blob_lines

class ReaperProject:

    def __init__(self, path):
        self.path = path
        self.lines = []

    def read(self):
        # Check if the file exists
        if not os.path.isfile(self.path):
            raise FileNotFoundError("File not found: " + self.path)
        # Read reaper.rpp project file
        with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        self.lines = data.splitlines()

    def find_plugin_instances(self, name):
        # Find all Dexed instances
        plugin_instances = []
        plugin_line_numbers = [i for i, line in enumerate(self.lines) if line.lstrip().startswith('<VST "VST3i: ' + name)]
        for plugin_line_number in plugin_line_numbers:
            # print("Plugin instance begin line number: " + str(plugin_line_number))
            PI = PluginInstance(self.lines, plugin_line_number)
            plugin_instances.append(PI)
        return plugin_instances

    def write(self, path):
        # Write the modified project file
        with open(path, 'w') as f:
            f.write('\n'.join(self.lines))

def print_blobs(plugin_instance):
    print("Decoded blob 1 in hex: " + plugin_instance.blobs[0].hex()) # Meaning unclear; does it contain the DX7 In and DX7 Out MIDI ports?
    print("Decoded blob 2:")
    DS = dexed.DexedState()
    DS.parse_data_blob(plugin_instance.blobs[1])
    print(DS)
    preset_name = plugin_instance.blobs[2].decode('ascii').split('\x00')[1].split('\x00')[0]
    print("Preset name from blob 3: " + preset_name)

def main():
    rpp = ReaperProject(os.path.dirname(__file__) + '/reaper.rpp')
    rpp.read()
    initial_number_of_lines = len(rpp.lines)

    for plugin_instance in rpp.find_plugin_instances("Dexed"):
        # NOTE: This only works as long as editing the plugin_instance object does not change the number of lines in rpp.lines;
        # if it did, the line numbers of the other plugin instances would be wrong and we would have to find them again in each iteration
        # (this is probably where we would need to start using the UUIDs of the plugin instances)
        print("Plugin instance begin line number: " + str(plugin_instance.begin_line_number))
        print("Plugin instance end line number: " + str(plugin_instance.end_line_number))
        print("Plugin instance intendation level: " + str(plugin_instance.intendation_level))

        print("ORIGINAL BLOBS:")
        print_blobs(plugin_instance)

        DS = dexed.DexedState()

        DS.parse_data_blob(plugin_instance.blobs[1])

        # Edit dexed_state_dict here
        DS.dexed_state_dict['dexedState']['@currentProgram'] = "0" # This does not actually change the loaded voice; to do that, change the ['dexedState']['dexedBlob']['@program']
        # DS.dexed_state_dict['dexedState']['@opSwitch'] = "000001" # Only operator 1 is on; seems to change when another program is loaded from the Dexed UI
        # DS.dexed_state_dict['dexedState']['@wheelMod'] = "7 1 1 1"
        # DS.dexed_state_dict['dexedState']['@footMod'] = "8 1 1 1"
        # DS.dexed_state_dict['dexedState']['@breathMod'] = "9 1 1 1"
        # DS.dexed_state_dict['dexedState']['@aftertouchMod'] = "10 1 1 1"
        DS.dexed_state_dict['dexedState']['@engineType'] = "0" # Modern
        
        # Edit the loaded bank of voices in dexed_state_dict
        sysex = dx7.make_init_bank_sysex()
        sysex_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in sysex])
        DS.dexed_state_dict['dexedState']['dexedBlob']['@sysex'] = sysex_hex

        # Edit the currently loaded voice in dexed_state_dict to match the current program
        program = dx7.get_vced_from_bank_sysex(sysex, int(DS.dexed_state_dict['dexedState']['@currentProgram'])) + [0x20, 0x00, 0x00, 0x00, 0x00, 0x00] # TODO: Document what these bytes mean
        program_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in program])
        DS.dexed_state_dict['dexedState']['dexedBlob']['@program'] = program_hex
        
        plugin_instance.update_blob(1, (DS.get_data_blob()))

        print("MODIFIED BLOBS:")
        print_blobs(plugin_instance)
    
    assert len(rpp.lines) == initial_number_of_lines
    rpp.write(os.path.dirname(__file__) + '/reaper_modified.rpp')

if __name__ == "__main__":
    main()