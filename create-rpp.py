#!/usr/bin/env python3

# pip install --upgrade attrs ply

# Add the rppgit subdirectory to the path
import sys, base64, math

sys.path.append("rppgit") # Rename rpp git directory so it doesn't conflict with the rpp module

# Load the rpp module from the rpp subdirectory; DO NOT load rpp from the current directory
import rpp
import dx7
import dx7II

print(dir(rpp))

# Load dx7IId.rpp into a string
with open("dx7IId.rpp", "r") as f:
    s = f.read()

# Create a new project
r = rpp.loads(s)

# Find all Dexed instances
all_vsts = r.findall('.//VST') # Find all VST tags; TODO: Limit to Dexed VSTs
dexed_instances = []
for instance in all_vsts:
    if instance.attrib[1] == "Dexed.vst3":
        dexed_instances.append(instance)
assert len(dexed_instances) == 128

# Find all "midi/midi_note_filter" JS tags
all_jss = r.findall('.//JS') # Find all JS tags
midi_note_filters = []
for js in all_jss:
    if js.attrib[0] == "midi/midi_note_filter":
        midi_note_filters.append(js)
print(len(midi_note_filters))
assert len(midi_note_filters) == 128

# Find all "utility/volume_pan" JS tags
volume_pans = []
for js in all_jss:
    if js.attrib[0] == "utility/volume_pan":
        volume_pans.append(js)

import reaper
import dexed

def get_dexed_state(instance):
    if not instance.attrib[1] == "Dexed.vst3":
        return
    # Parse lines into 3 blobs: 1st line = 1st blob, last line = 3rd blob, everything in between without whitespace = 2nd blob
    blobs = []
    # 1st blob: the first line
    blobs.append(instance.children[0])
    # 2nd blob: everything between the first and last line
    blobline = ""
    for line in instance.children[1:-1]:
        if not line.strip() == "":
            blobline += line
    blobs.append(blobline)
    # 3rd blob: the last line
    blobs.append(instance.children[-1])
    # Decode the second blob
    decoded_blob1 = base64.b64decode(blobs[1])
    DS = dexed.DexedState()
    DS.parse_data_blob(decoded_blob1)
    return DS

def set_dexed_state(instance, DexedState):
    DS = DexedState
    new_decoded_blob1 = DS.get_data_blob()
    # Encode the modified blob back to base64; TODO: Move this to a function
    new_blob1 = base64.b64encode(new_decoded_blob1)
    # Convert to a string but without the b' and ' characters
    new_blob1 = new_blob1.decode('ascii')
    # Split into lines of 128 characters
    blob_lines = [new_blob1[i:i+128] for i in range(0, len(new_blob1), 128)]
    # Construct new children
    new_children = []
    new_children.append(instance.children[0])
    for blob_line in blob_lines:
        new_children.append(blob_line)
    new_children.append(instance.children[-1])
    instance.children = new_children


def get_sysex_program_number(i):
    # i can be 0 to 127
    # Get the sysex, the program, and the number of the voice in the bank
    i_is_uneven = i % 2 == 1

    filename = "DX7IIFDVoice"
    if 0 <= i < 32:
        filename += "32"
    elif 32 <= i < 64:
        filename += "64"
    elif 64 <= i < 96:
        filename += "32B"
    elif 96 <= i < 128:
        filename += "64B"
    filename += ".SYX"

    print("Filename:", filename)

    # Load sysex from file
    f = open(filename, "rb")
    sysex = f.read()
    f.close()

    # Determine the voice number
    # For 0 to 31, j is 0 to 31; for 32 to 63, j is 0 to 31, for 64 to 95, j is 0 to 31, etc.
    voice_number = i % 32
    print("Voice number:", voice_number)

    vced = dx7.load_vced_from_file(filename, voice_number)

    return sysex, vced, voice_number

i = 0
j = 0
n = 0
voice_names = []
detuned_performance_names = []

for instance in dexed_instances:
    DS = get_dexed_state(instance)

    n_is_uneven = n%2 == 1


    # Read a PCED from a file
    if n < 64:
        performance_filename = "DX7IIFDPerf.SYX"
    else:
        performance_filename = "DX7IIFDPerfB.SYX"
    PS = dx7II.PerformanceSyx(performance_filename)

    print("Performance:", PS.pceds[j].pnam)
    print("i:", i, "j:", j, "n:", n)
    voice_nr = 0
    if n_is_uneven:
        print("Voice B:", PS.pceds[j].vnmb)
        voice_nr = PS.pceds[j].vnmb
    else:
        print("Voice A:", PS.pceds[j].vnma)
        voice_nr = PS.pceds[j].vnma

    split_point = PS.pceds[j].sppt
    print("Split point:", split_point)

    # Decibel reduction for dual and split modes to prevent clipping
    number_of_voices = 2
    reduction = 20 * math.log10(1 / math.sqrt(number_of_voices))
    reduction = round(reduction, 1)

    if PS.pceds[j].plmd == 0:
        print("Mode: Poly")
        midi_note_filters[n].children[0][0] = "0"
        midi_note_filters[n].children[0][1] = "127"
        volume_pans[n].children[0][0] = str(reduction)
    elif PS.pceds[j].plmd == 1:
        print("Mode: Dual")
        midi_note_filters[n].children[0][0] = "0"
        midi_note_filters[n].children[0][1] = "127"
        volume_pans[n].children[0][0] = str(reduction)
    elif PS.pceds[j].plmd == 2:
        print("Mode: Split")
        if n_is_uneven:
            midi_note_filters[n].children[0][0] = str(split_point)
            midi_note_filters[n].children[0][1] = "127"
        else:
            midi_note_filters[n].children[0][0] = "0"
            midi_note_filters[n].children[0][1] = str(split_point -1)
        volume_pans[n].children[0][0] = "-0.0" # No reduction since only one voice is active at a time due to the split point

    ###
    # TODO: Figure out how this stuff works
    volume_balance = PS.pceds[j].blnc
    print("Volume balance:", volume_balance)
    pan_mode = PS.pceds[j].pnmd
    print("Pan mode:", pan_mode)
    pan_control_range = PS.pceds[j].panrng
    print("Pan control range:", pan_control_range)
    ###

    # Detune
    dual_detune = PS.pceds[j].ddtn
    if dual_detune != 0:
        detuned_performance_names.append(PS.pceds[j].pnam)
    print("Dual detune:", dual_detune)
    # Convert detune value to what Dexed masterTune expects: -1398101 .. 1398101 # TODO: Check whether this is correct; why 1398101?
    # This amount is likely far too much. We need to find out how Dexed converts the detune value to cents.
    converted_detune = int(dual_detune) / 7 * 1398101
    if n_is_uneven:
        DS.dexed_state_dict['dexedState']['@masterTune'] = str(converted_detune)
    else:
        DS.dexed_state_dict['dexedState']['@masterTune'] = "-" + str(converted_detune)

    print(midi_note_filters[n].children[0])
    print(volume_pans[n].children[0])

    sysex, vced, voice_number = get_sysex_program_number(voice_nr)
    voice_name = dx7.get_voice_name(vced)
    print("Voice name:", voice_name)
    voice_names.append(voice_name)

    # Set the currently selected program
    DS.set_program(vced)

    # Without setting sysex, the program is not loaded correctly.
    # This is a pity because it means we always need to load 32 voices even if we only want to load one.
    DS.set_sysex(sysex)

    # Set the currently selected voice
    DS.dexed_state_dict['dexedState']['@currentProgram'] = str(voice_number)

    set_dexed_state(instance, DS)
    print("")
    
    i += 1
    n += 1
    if n_is_uneven:
        j += 1
    if i == 32:
        i = 0
    if j == 32:
        j = 0

# From both performance files, get the performance names
performance_names = []
performance_filenames = ["DX7IIFDPerf.SYX", "DX7IIFDPerfB.SYX"]
for performance_filename in performance_filenames:
    PS = dx7II.PerformanceSyx(performance_filename)
    for i in range(32):
        performance_names.append(PS.pceds[i].pnam)
assert len(performance_names) == 64
assert len(voice_names) == 128

# Find all CONTAINER tags and set the names of the containers
containers = r.findall('.//CONTAINER')
print("Number of containers:", len(containers))
assert len(containers) == 128
i_container = 0
for container in containers:
    # Set the name of the container (name is the 2nd property)
    container.attrib[1] = voice_names[i_container]
    i_container += 1

# Find all TRACK tags and set the names of the tracks
tracks = r.findall('.//TRACK')
print("Number of tracks:", len(tracks))
assert len(tracks) == 64
i_track = 0
for track in tracks:
    # Set the name of the tracks
    track.children[0] = "NAME", performance_names[i_track].strip() # FIXME: Is there a cleaner way to do this?
    i_track += 1

# Write the modified project file
with open("dx7IId_modified.rpp", "w") as f:
    f.write(rpp.dumps(r))

print("Detuned performances:")
for detuned_performance_name in detuned_performance_names:
    print(detuned_performance_name)