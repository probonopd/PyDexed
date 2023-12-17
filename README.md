# PyDexed

Python scripts to modify Reaper RPP files containing Dexed instances

- [x] Read Dexed plugin state XML from Reaper RPP file
- [x] Alternatively, read Dexed plugin state XML from Dexed savestate file
- [x] Decode Dexed plugin state XML to Python dictionary
- [x] Decode `sysex` and `program` Dexed plugin state parameters (encoded using JUCE non-standard base64 encoding) to hex
- [x] Encode hex to Dexed plugin state parameters (encoded using JUCE non-standard base64 encoding)
- [x] Encode Python dictionary to Dexed plugin state XML
- [x] Make changes to Dexed plugin state in a Reaper RPP file and write changed Reaper RPP file
- [ ] Convert MiniDexed `performance.ini` to Reaper RPP files
- [ ] Generate Reaper RPP files for TX816 performances
- [ ] ...
