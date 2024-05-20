# PyDexed

Python scripts to modify Reaper RPP files containing Dexed instances.

The objective is to reconstruct TX816-like performances in Reaper, roughly like this:

![image](https://github.com/probonopd/PyDexed/assets/2480569/6a0e9f08-3ca3-4015-a25a-5036727ea7b5)

- [x] Read Dexed plugin state XML from Reaper RPP file
- [x] Alternatively, read Dexed plugin state XML from Dexed savestate file
- [x] Decode Dexed plugin state XML to Python dictionary
- [x] Decode `sysex` and `program` Dexed plugin state parameters (encoded using JUCE non-standard base64 encoding) to hex
- [x] Encode hex to Dexed plugin state parameters (encoded using JUCE non-standard base64 encoding)
- [x] Encode Python dictionary to Dexed plugin state XML
- [x] Make changes to Dexed plugin state in a Reaper RPP file and write changed Reaper RPP file (e.g, change the loaded bank of voices and the currently loaded voice)
- [ ] Convert MiniDexed `performance.ini` to Reaper RPP files __(WIP)__
- [ ] Generate Reaper RPP files for TX816 performances __(WIP)__
- [ ] Do the same for Ableton Live __(WIP)__
- [ ] ...
