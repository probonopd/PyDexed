#!/usr/bin/env python3

from reaper import *

def main():
    rpp = ReaperProject(os.path.dirname(__file__) + '/tx816_structure.rpp')
    rpp.read()
    initial_number_of_lines = len(rpp.lines)

    number_of_dexed_instances = len(rpp.find_plugin_instances("Dexed"))
    print("Number of Dexed instances: " + str(number_of_dexed_instances))

    i = 0
    for plugin_instance in rpp.find_plugin_instances("Dexed"):
        # NOTE: This only works as long as editing the plugin_instance object does not change the number of lines in rpp.lines;
        # if it did, the line numbers of the other plugin instances would be wrong and we would have to find them again in each iteration
        # (this is probably where we would need to start using the UUIDs of the plugin instances)

        DS = dexed.DexedState()
        DS.parse_data_blob(plugin_instance.blobs[1])

        # Edit dexed_state_dict here
                
        # For the first 8 plugin instances, set the program to 0, for the next 8 plugin instances, set the program to 1, and so on
        program = i // 8
        print ("Setting instance " + str(i) + " to program " + str(program))
        i += 1
        DS.dexed_state_dict['dexedState']['@currentProgram'] = str(program)

        # NOTE: This does not actually change the loaded voice; to do that, change the ['dexedState']['dexedBlob']['@program']

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
    
    assert len(rpp.lines) == initial_number_of_lines
    rpp.write(os.path.dirname(__file__) + '/reaper_modified.rpp')

if __name__ == "__main__":
    main()