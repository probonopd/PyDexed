#!/usr/bin/env python3

import inifile
import os
import urllib.request
import zipfile

from reaper import *
import tx816

def main():

    # Check if the file tx816_structure.zip exists
    if not os.path.isfile("tx816_structure.zip"):
        # Download the tx816_structure.zip file from GitHub
        print("Downloading tx816_structure.zip...")
        urllib.request.urlretrieve("https://github.com/probonopd/PyDexed/files/13707855/tx816_structure.zip", "tx816_structure.zip")
        print("Download complete.")

    # Check if the MDX_Vault-master.zip file exists
    if not os.path.isfile("MDX_Vault-main.zip"):
        # Download the MDX_Vault-master.zip file from GitHub
        print("Downloading MDX_Vault-main.zip...")
        urllib.request.urlretrieve("https://codeload.github.com/BobanSpasic/MDX_Vault/zip/refs/heads/main", "MDX_Vault-main.zip")
        print("Download complete.")

    # Check if the Dexed_cart_1.0.zip file exists
    if not os.path.isfile("Dexed_cart_1.0.zip"):
        # Download the Dexed_cart_1.0.zip file from GitHub
        print("Downloading Dexed_cart_1.0.zip...")
        urllib.request.urlretrieve("http://hsjp.eu/downloads/Dexed/Dexed_cart_1.0.zip", "Dexed_cart_1.0.zip")
        print("Download complete.")

    # Unzip the tx816_structure.rpp file from tx816_structure.zip
    with zipfile.ZipFile("tx816_structure.zip", 'r') as zip:
        filename = "tx816_structure.rpp"
        zip.extract(filename)

    rpp = ReaperProject('tx816_structure.rpp')
    rpp.read()
    os.remove('tx816_structure.rpp')

    initial_number_of_lines = len(rpp.lines)

    number_of_dexed_instances = len(rpp.find_plugin_instances("Dexed"))
    print("Number of Dexed instances: " + str(number_of_dexed_instances))

    track_names = []

    i = 0
    for plugin_instance in rpp.find_plugin_instances("Dexed"):
        track_number = i // 8
        tg_number = i % 8

        # Find the ini file for the current track number
        zipped_file = zipfile.ZipFile("MDX_Vault-main.zip")
        # Find a file in the zip file that starts with MDX_Vault-main/TX816/Factory/n+1, prepended with 0s, and followed by any number of characters + ".ini"
        # For instance, for n = 0, this would be "MDX_Vault-main/TX816/Factory/000001_Something.ini"
        for file in zipped_file.namelist():
            if file.startswith("MDX_Vault-main/TX816/Factory/" + str(track_number+1).zfill(6)) and file.endswith(".ini"):
                ini_file_name = file
                break
        
        track_name = os.path.basename(ini_file_name)
        track_name = track_name[track_name.find('_')+1:track_name.rfind('.')]
        print(track_name,  "(TG" + str(tg_number+1) + ")")
        if track_name not in track_names:
            track_names.append(track_name)

        # Read the ini file
        with zipped_file.open(ini_file_name) as file:
            ini_file = file.read()
            # Extract the ini file to the current directory
            with open(os.path.basename(ini_file_name), 'wb') as f:
                f.write(ini_file)

        # print("Loading ini file: " + ini_file_name)
        ini = inifile.IniFile(os.path.basename(ini_file_name))
        # Delete the ini file
        os.remove(os.path.basename(ini_file_name))

        # Set the pan in the "JS utility/volume_pan" plugin
        panN_ini = ini.get('Pan' + str(tg_number+1))
        # Find the numbers of all lines that contain "<JS utility/volume_pan" after whitespace, and add 1 to each of them
        # (these are the lines that contain the volume and pan values for the Dexed instances)
        volume_pan_line_number = [i+1 for i, line in enumerate(rpp.lines) if line.lstrip().startswith('<JS utility/volume_pan')][tg_number]
        # Get the number of leading spaces in the line
        indent = len(rpp.lines[volume_pan_line_number]) - len(rpp.lines[volume_pan_line_number].lstrip())
        # This line contains multiple fields, each separated by a space
        fields = rpp.lines[volume_pan_line_number].strip().split(' ')
        # Replace the 2nd field (the pan) with -100 to 100
        # panN_ini goes from 0 to 127, so we need to convert it to -100 to 100
        converted_pan = int(panN_ini) * 200 / 127 - 100
        allowed_values = [-100, -66, -50, -33, -25, -10, -5, 0, 5, 10, 25, 33, 50, 66, 100]
        # Find the closest allowed value
        converted_pan = min(allowed_values, key=lambda x:abs(x-converted_pan))
        # print("Original pan: " + panN_ini + ", converted pan: " + str(converted_pan))
        fields[1] = str(converted_pan)
        # Replace the line with the modified line
        rpp.lines[volume_pan_line_number] = ' ' * indent + ' '.join(fields)
        # print(rpp.lines[volume_pan_line_number])

        # NOTE: This only works as long as editing the plugin_instance object does not change the number of lines in rpp.lines;
        # if it did, the line numbers of the other plugin instances would be wrong and we would have to find them again in each iteration
        # (this is probably where we would need to start using the UUIDs of the plugin instances)

        DS = dexed.DexedState()
        DS.parse_data_blob(plugin_instance.blobs[1])

        # Edit dexed_state_dict here
                
        # For the first 8 plugin instances, set the program to 0, for the next 8 plugin instances, set the program to 1, and so on
        # print ("Setting instance " + str(i) + " to program " + str(track_number))
        i += 1
        DS.dexed_state_dict['dexedState']['@currentProgram'] = str(track_number)

        # NOTE: This does not actually change the loaded voice; to do that, change the ['dexedState']['dexedBlob']['@program']

        DS.dexed_state_dict['dexedState']['@opSwitch'] = "111111" # Seems to change when another program is loaded from the Dexed UI

        cutoffN_ini = ini.get('Cutoff' + str(tg_number+1)) # 0 .. 99
        converted_cutoff = round(int(cutoffN_ini) / 99, 1) #  Dexed expects: 0.0 .. 1.0
        DS.dexed_state_dict['dexedState']['@cutoff'] = converted_cutoff

        resonanceN_ini = ini.get('Resonance' + str(tg_number+1)) # 0 .. 99
        converted_resonance = round(int(resonanceN_ini) / 99, 1) #  Dexed expects: 0.0 .. 1.0
        DS.dexed_state_dict['dexedState']['@reso'] = converted_resonance

        volumeN_ini = int(ini.get('Volume' + str(tg_number+1))) # 0 .. 99
        converted_gain = volumeN_ini / 99 #  Dexed expects: 0.0 .. 1.0
        converted_gain = round(converted_gain, 1)
        DS.dexed_state_dict['dexedState']['@gain'] = converted_gain

        monoModeN_ini = ini.get('MonoMode' + str(tg_number+1)) # 0 .. 1
        converted_monoMode = int(monoModeN_ini) #  Dexed expects: 0 .. 1
        DS.dexed_state_dict['dexedState']['@monoMode'] = str(converted_monoMode)

        DS.dexed_state_dict['dexedState']['@engineType'] = "0" # Modern

        # Change the detune according to the detuneN in the ini file
        detuneN_ini = ini.get('Detune' + str(tg_number+1)) # -99 .. 99
        # Convert detune value to what Dexed masterTune expects: -1398101 .. 1398101 # TODO: Check whether this is correct; why 1398101?
        converted_detune = int(detuneN_ini) / 99 * 1398101
        # Round to 0 decimal places
        converted_detune = int(round(converted_detune, 0))
        # print("Original detune: " + detuneN_ini + ", converted detune: " + str(converted_detune))
        DS.dexed_state_dict['dexedState']['@masterTune'] = str(converted_detune)

        # Edit the loaded bank of voices in dexed_state_dict
        zipped_file = zipfile.ZipFile("Dexed_cart_1.0.zip")
        # "Dexed_cart_1.0/Original Yamaha/TX816/Tfi1.syx" for instance 0, "Tfi2.syx" for instance 1,
        # "Tfi1.syx" again for instance 8, "Tfi2.syx" again for instance 9, and so on
        for file in zipped_file.namelist():
            if file.startswith("Dexed_cart_1.0/Original Yamaha/TX816/Tfi" + str((i-1)%8+1) + ".syx"):
                sysex_file_name = file
                break
        # Extract the sysex file to the current directory
        with zipped_file.open(sysex_file_name) as file:
            sysex = file.read()
            with open(os.path.basename(sysex_file_name), 'wb') as f:
                f.write(sysex)
        # print("Loading sysex file: " + sysex_file_name)
        with open(os.path.basename(sysex_file_name), 'rb') as file:
            sysex = file.read()
        # Delete the sysex file
        os.remove(os.path.basename(sysex_file_name))
        sysex_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in sysex])
        DS.dexed_state_dict['dexedState']['dexedBlob']['@sysex'] = sysex_hex

        # Edit the currently loaded voice in dexed_state_dict to match the current program
        vced = dx7.get_vced_from_bank_sysex(sysex, int(DS.dexed_state_dict['dexedState']['@currentProgram']))
        program = vced + [0x20, 0x00, 0x00, 0x00, 0x00, 0x00] # TODO: Document what these bytes mean
        program_hex = ' '.join([hex(b)[2:].zfill(2).upper() for b in program])
        DS.dexed_state_dict['dexedState']['dexedBlob']['@program'] = program_hex

        # Get the name of the voice from the VCED
        name = dx7.get_voice_name(vced)
        print("Voice name from VCED: " + name)

        # Construct the dexed_state_dict['dexedState']['@wheelMod'] value given the above format, based on the content of tx816 function_data
        # For example, if the voice name is "AC.PNO 1.1", then dexed_state_dict['dexedState']['@wheelMod'] should be
        # "66 1 0 0" because the "R MOD" value for this voice is 66, and the "P MOD", "A MOD", and "E MOD" values are 1, 0, and 0 respectively
            
        # Find the voice in tx816 function_data
        voice = [voice for voice in tx816.function_data if voice["Voice"] == name][0]
        assert voice["Voice"] == name
        # Construct the dexed_state_dict['dexedState']['@wheelMod'] value given the above format, based on the content of tx816 function_data
        converted_wheelMod = voice["R MOD"] + " " + voice["P MOD"] + " " + voice["A MOD"] + " " + voice["E MOD"]
        print("Converted wheelMod: " + converted_wheelMod)
        DS.dexed_state_dict['dexedState']['@wheelMod'] = converted_wheelMod
        converted_aftertouchMod = voice["R A.TCH"] + " " + voice["P A.TCH"] + " " + voice["A A.TCH"] + " " + voice["E A.TCH"]
        print("Converted aftertouchMod: " + converted_aftertouchMod)
        DS.dexed_state_dict['dexedState']['@aftertouchMod'] = converted_aftertouchMod
        converted_footMod = voice["R F.C"] + " " + voice["P F.C"] + " " + voice["A F.C"] + " " + voice["E F.C"]
        print("Converted footMod: " + converted_footMod)
        DS.dexed_state_dict['dexedState']['@footMod'] = converted_footMod
        converted_breathMod = voice["R B.C"] + " " + voice["P B.C"] + " " + voice["A B.C"] + " " + voice["E B.C"]
        print("Converted breathMod: " + converted_breathMod)
        DS.dexed_state_dict['dexedState']['@breathMod'] = converted_breathMod
        print("")

        
        plugin_instance.update_blob(1, (DS.get_data_blob()))
    
    # Find all lines that contain '<CONTAINER Container ""' after whitespace and name them like this:
    # TG1, TG2, TG3, TG4, TG5, TG6, TG7, TG8, then start again with TG1, TG2, etc.
    i = 1
    for line in rpp.lines:    
        if '<CONTAINER Container ""' in line:
            rpp.lines[rpp.lines.index(line)] = line.replace('<CONTAINER Container ""', '<CONTAINER Container "TG' + str(i) + '"')
            i += 1
            if i > 8:
                i = 1

    # Find all lines that contain 'NAME ""' after whitespace and use track_names to name them
    i = 0
    for line in rpp.lines:    
        if 'NAME ""' in line:
            rpp.lines[rpp.lines.index(line)] = line.replace('NAME ""', 'NAME "' + track_names[i] + '"')
            i += 1


    assert len(rpp.lines) == initial_number_of_lines
    rpp.write('tx816.rpp')

    # Zip the project file
    with zipfile.ZipFile('tx816.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write('tx816.rpp')

    print("Done.")
    print(os.path.abspath('tx816.rpp'))
    print(os.path.abspath('tx816.zip'))

if __name__ == "__main__":
    main()