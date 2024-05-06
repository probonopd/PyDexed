#!/usr/bin/env python3

# pip install --upgrade attrs ply

# Add the rppgit subdirectory to the path
import sys, os, base64, math, zipfile
import urllib.request

# If directory "rppgit" does not exist, clone the "rpp" git repository
# but rename rpp git directory "rppgit" so it doesn't conflict with the "rpp" module
if not os.path.isdir("rppgit"):
    os.system("git clone https://github.com/Perlence/rpp rppgit")

sys.path.append("rppgit")

# Load the rpp module from the rpp subdirectory; DO NOT load rpp from the current directory
import rpp
import dx7
import dx7II

print(dir(rpp))

# Check if the file tx816_structure.zip exists
if not os.path.isfile("dx7IId_structure.zip"):
    # Download the tx816_structure.zip file from GitHub
    print("Downloading dx7IId_structure.zip...")
    urllib.request.urlretrieve("https://github.com/probonopd/PyDexed/releases/download/input/dx7IId_structure.zip", "dx7IId_structure.zip")
    print("Download complete.")

# Check if the file Dexed_cart_1.0.zip exists
if not os.path.isfile("Dexed_cart_1.0.zip"):
    # Download the Dexed_cart_1.0.zip file
    print("Downloading Dexed_cart_1.0.zip...")
    urllib.request.urlretrieve("http://hsjp.eu/downloads/Dexed/Dexed_cart_1.0.zip", "Dexed_cart_1.0.zip")
    print("Download complete.")

# Check if the file DX7IIfd.ROM1A.zip exists
if not os.path.isfile("DX7IIfd.ROM1A.zip"):
    # Download the Dexed_cart_1.0.zip file
    print("Downloading DX7IIfd.ROM1A.zip...")
    urllib.request.urlretrieve("https://github.com/probonopd/PyDexed/releases/download/input/DX7IIfd.ROM1A.zip", "DX7IIfd.ROM1A.zip") # Mirrored from https://github.com/asb2m10/dexed/issues/165#issuecomment-1436586010
    print("Download complete.")
    
# Unzip the dx7IId_structure.rpp file from dx7IId_structure.zip
with zipfile.ZipFile("dx7IId_structure.zip", 'r') as zip:
    filename = "dx7IId_structure.rpp"
    zip.extract(filename)

# Unzip Dexed_cart_1.0.zip
zip_file_path = 'Dexed_cart_1.0.zip'
extract_directory = 'Dexed_cart_1.0/Original Yamaha/DX7IIFD'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        print(file_info)
        if file_info.filename.startswith(extract_directory):
            print("Extracting %s" % file_info)
            zip_ref.extract(file_info, path=os.getcwd())

# Unzip DX7IIfd.ROM1A.zip
zip_file_path = 'DX7IIfd.ROM1A.zip'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        zip_ref.extract(file_info, path=os.getcwd())

# Load dx7IId.rpp into a string
with open("dx7IId_structure.rpp", "r") as f:
    s = f.read()
os.remove('dx7IId_structure.rpp')

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
# (used to set the lowest and highest note for each voice for split mode defined in DX7II performance PCED)
all_jss = r.findall('.//JS') # Find all JS tags
midi_note_filters = []
for js in all_jss:
    if js.attrib[0] == "midi/midi_note_filter":
        midi_note_filters.append(js)
print(len(midi_note_filters))
assert len(midi_note_filters) == 128

# Find all "utility/volume_pan" JS tags
# (used to set the stereo pan, and to set the volume reduction for dual and split modes defined in DX7II performance PCED)
volume_pans = []
for js in all_jss:
    if js.attrib[0] == "utility/volume_pan":
        volume_pans.append(js)

# Find all "IX/MIDI_Router" JS tags
# (used to set the additional note shift = additional transpose defined in DX7II performance PCED)
midi_routers = []
for js in all_jss:
    if js.attrib[0] == "IX/MIDI_Router":
        midi_routers.append(js)

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

# AMEM, which can be converted to ACED, is contained in 'DX7IIfd ROM1A.zip' from
# https://github.com/asb2m10/dexed/issues/165#issuecomment-1436586010
# There are 32 performances x 35 bytes AMEM data = 1120 bytes AMEM data in each of the 2 syx files
# starting at offset 16178 (0x3F82) according to
# https://github.com/BobanSpasic/MDX_PerfConv/issues/5#issuecomment-1807177759
full_dumps = ["DX7IIfd ROM1A 1-32.syx", "DX7IIfd ROM1A 33-64.syx"]
# Extract the AMEM data from the syx files
amems = []
for full_dump in full_dumps:
    f = open(full_dump, "rb")
    dump = f.read()
    f.close()
    # Extract the AMEM data from the dump
    for i in range(32):
        amem = dump[16178 + i*35:16178 + i*35 + 35]
        amems.append(amem)
print("Number of AMEMs:", len(amems))
# Convert the AMEM data to ACED data
aceds = []
for amem in amems:
    aced = dx7II.amem2aced(amem)
    a = dx7II.aced()
    a.set_bytes(aced)
    aceds.append(a)

# TODO: While we're at it, we might also extract the VCEDs and PCEDs from the syx files in the same way
# instead of using other syx files for them below

i = 0
j = 0
n = 0
performance_names = []
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

    performance_name = PS.pceds[j].pnam.strip()
    print("Performance:", performance_name)
    
    print("i:", i, "j:", j, "n:", n)

    split_point = PS.pceds[j].sppt
    print("Split point:", split_point)

    # Decibel reduction for dual and split modes to prevent clipping
    number_of_voices = 2
    reduction = 20 * math.log10(1 / math.sqrt(number_of_voices))
    reduction = round(reduction, 1)

    is_unison = False

    if PS.pceds[j].plmd == 0:
        print("Mode: Single")
        midi_note_filters[n].children[0][0] = "0" # Lowest sounding note
        midi_note_filters[n].children[0][1] = "127" # Highest sounding note
        # Check if unison is enabled in the ACED; pmod bit1: unison on/off
        if aceds[j].pmod & 0b10 == 0b10:
            is_unison = True
            performance_name += " (Single, Unison)"
            volume_pans[n].children[0][0] = str(reduction) # Reduce volume because two voices are active at the same time
        else:
            performance_name += " (Single)"
            volume_pans[n].children[0][0] = "-0.0" # No reduction since only one voice is active at a time
            volume_pans[n].children[0][1] = "50" # Center pan since only one voice is active at a time
            if n_is_uneven:
                # Set voice B to be silent
                midi_note_filters[n].children[0][0] = "0" # Lowest sounding note
                midi_note_filters[n].children[0][1] = "0" # Highest sounding note

    elif PS.pceds[j].plmd == 1:
        print("Mode: Dual")
        performance_name += " (Dual)"
        midi_note_filters[n].children[0][0] = "0" # Lowest sounding note
        midi_note_filters[n].children[0][1] = "127" # Highest sounding note
        volume_pans[n].children[0][0] = str(reduction) # Reduce volume because two voices are active at the same time
    elif PS.pceds[j].plmd == 2:
        print("Mode: Split")
        performance_name += " (Split)"
        if n_is_uneven:
            # Voice B
            midi_note_filters[n].children[0][0] = str(split_point) # Lowest sounding note
            midi_note_filters[n].children[0][1] = "127" # Highest sounding note
        else:
            # Voice A
            midi_note_filters[n].children[0][0] = "0" # Lowest sounding note
            midi_note_filters[n].children[0][1] = str(split_point -1) # Highest sounding note
        volume_pans[n].children[0][0] = "-0.0" # No reduction since only one voice is active at a time due to the split point

    # Volume balance (Note: DX7II Pan Modes are currently not supported)
    volume_balance = PS.pceds[j].blnc
    if volume_balance != 50:
        performance_name = performance_name.replace(")", ", Volume Balance " + str(volume_balance) + ")")
        print("Volume balance:", volume_balance)
        # If volume balance is 50, then the volume of voice A and B is unchanged.
        # Educated guess (to be verified):
        # If the volume balance is 0, then voice B is silent and voice A is at full volume.
        # If the volume balance is 100, then voice A is silent and voice B is at full volume.
        # If the volume balance is 25, then voice A is at 75% volume and voice B is at 25% volume.
        # volume_pans[n].children[0][0] expects a value in decibels, so we need to convert the volume balance to decibels like so:
        old_volume_adjustment = float(volume_pans[n].children[0][0]) # Decibels
        if n_is_uneven:
            # Voice B
            new_volume_adjustment = old_volume_adjustment + (volume_balance - 50) / 2
        else:
            # Voice A
            new_volume_adjustment = old_volume_adjustment + (50 - volume_balance) / 2
        volume_pans[n].children[0][0] = str(new_volume_adjustment)

    # Detune
    unsion_detune = aceds[j].udtn
    dual_detune = PS.pceds[j].ddtn
    total_detune = unsion_detune + dual_detune
    if total_detune != 0:
        performance_name = performance_name.replace(")", ", Detuned)")
        if n_is_uneven:
            detuned_performance_names.append(performance_name)
    print("Total detune:", total_detune)
    # Convert detune value to what Dexed masterTune expects: -1398101 .. 1398101 # TODO: Check whether this is correct; why 1398101?
    # According to the DX7II manual, when dual detune is 0, the detune is 0 cents. When it is 7, the detune is 1/4 step (50 cents) up and 1/4 step (50 cents) down
    # 1 semitone = 1/2 step = 100 cents. So 1/4 step = 50 cents
    # The maximum detune in Dexed is 1 semitone up and 1 semitone down, so 100 cents up and 100 cents down. (-1398101 .. 1398101)
    converted_detune = int(total_detune) / 7 * 1398101 / 2
    if n_is_uneven:
        DS.dexed_state_dict['dexedState']['@masterTune'] = str(converted_detune)
    else:
        DS.dexed_state_dict['dexedState']['@masterTune'] = "-" + str(converted_detune)

    voice_nr = 0

    if not is_unison:
        if n_is_uneven:
            print("Voice B:", PS.pceds[j].vnmb)
            voice_nr = PS.pceds[j].vnmb
        else:
            print("Voice A:", PS.pceds[j].vnma)
            voice_nr = PS.pceds[j].vnma
    else:
        print ("Unison:", PS.pceds[j].vnma)
        voice_nr = PS.pceds[j].vnma
            
    sysex, vced, voice_number = get_sysex_program_number(voice_nr)
    voice_name = dx7.get_voice_name(vced)

    # Note shift
    # 24 means no shift. 12 means 1 octave down, 36 means 1 octave up; 0 means 2 octaves down, 48 means 2 octaves up
    # Dexed has 0 as no shift. So we need to convert the note shift value from the DX7II to the Dexed value by subtracting 24
    if n_is_uneven:
        note_shift = PS.pceds[j].nsftb
    else:
        note_shift = PS.pceds[j].nsfta
    if note_shift != 24:
        converted_note_shift = note_shift - 24
        voice_name += " (Note Shift " + str(converted_note_shift) + ")"
        print("Additional note shift:", converted_note_shift)
        midi_routers[n].children[0][5] = str(converted_note_shift) # Additional note shift (in addition to what the voice data already specifies)
    else:
        midi_routers[n].children[0][5] = "0" # No additional note shift

    print("Voice name:", voice_name)
    voice_names.append(voice_name)

    # Set the currently selected program
    DS.set_program(vced)

    # Without setting sysex, the program is not loaded correctly.
    # This is a pity because it means we always need to load 32 voices even if we only want to load one.
    DS.set_sysex(sysex)

    # Set the currently selected voice
    DS.dexed_state_dict['dexedState']['@currentProgram'] = str(voice_number)

    # Set mod wheel, foot controller, breath controller, and aftertouch
    # TODO: Check whether this logic is correct (most likely not)
    # Dexed has a matrix for Wheel, Foot, Breath, Aftertouch x Pitch, Amp, EG Bias = 12 fields that can be set to 0 or 1,
    # prepended by the amount. But the DX7II ACED allows to set different amounts for pitch, amp, and eg bias.
    # So we need to convert the DX7II values to a single amount for each source; for now, let's use the maximum among the 3 sources.
    wheel_amount = max(aceds[j].mwpm, aceds[j].mwam, aceds[j].mweb)
    wheel_pitch_on = 1 if aceds[j].mwpm > 0 else 0
    wheel_amp_on = 1 if aceds[j].mwam > 0 else 0
    wheel_eg_bias_on = 1 if aceds[j].mweb > 0 else 0
    DS.dexed_state_dict['dexedState']['@wheelMod'] = "%s %s %s %s" % (wheel_amount, wheel_pitch_on, wheel_amp_on, wheel_eg_bias_on)

    foot_amount = max(aceds[j].fc1pm, aceds[j].fc1am, aceds[j].fc1eb, aceds[j].fc1vl)
    foot_pitch_on = 1 if aceds[j].fc1pm > 0 else 0
    foot_amp_on = 1 if aceds[j].fc1am > 0 else 0
    foot_eg_bias_on = 1 if aceds[j].fc1eb > 0 else 0
    DS.dexed_state_dict['dexedState']['@footMod'] = "%s %s %s %s" % (foot_amount, foot_pitch_on, foot_amp_on, foot_eg_bias_on)

    breath_amount = max(aceds[j].bcpm, aceds[j].bcam, aceds[j].bceb, aceds[j].bcpb)
    breath_pitch_on = 1 if aceds[j].bcpm > 0 else 0
    breath_amp_on = 1 if aceds[j].bcam > 0 else 0
    breath_eg_bias_on = 1 if aceds[j].bceb > 0 else 0
    DS.dexed_state_dict['dexedState']['@breathMod'] = "%s %s %s %s" % (breath_amount, breath_pitch_on, breath_amp_on, breath_eg_bias_on)

    # TODO: Set Pitch Bend Range and Pitch Bend Step
    # It seems that here, too, DX7II ACED allows to set more than one value for pitch bend range and pitch bend step depending on the source.

    if n_is_uneven:
        performance_names.append(performance_name)

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
