#!/usr/bin/env python3
# performancelint.py
#
# Linter for MiniDexed performance INI files.
#
# This script checks MiniDexed performance INI files for:
#   - Presence of all required parameters for each Tone Generator (TG1-TG8)
#   - Correct value ranges and types for each parameter
#   - Correct formatting of VoiceData (156 hex bytes if present)
#   - Presence and validity of global effects parameters
#
# The spec followed is based on the official MiniDexed implementation and documentation as of 2025-05-27.
# See: https://github.com/probonopd/MiniDexed and the code in performanceconfig.cpp
#
# Usage: python3 performancelint.py [folder]
#        (defaults to 'tx816' if no folder is given)

import os
import sys
import re
import dx7

def lint_performance_ini(filepath):
    """
    Lint a MiniDexed performance INI file for spec compliance.
    Checks all TG parameters and global effects section.
    """
    errors = []
    with open(filepath, 'r') as f:
        # Ignore comments and blank lines
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith(';')]
    params = dict()
    for line in lines:
        if '=' not in line:
            errors.append(f"Malformed line: {line}")
            continue
        k, v = line.split('=', 1)
        params[k.strip()] = v.strip()

    # Find how many TGs are present by checking for VoiceDataN or MIDIChannelN keys
    tg_numbers = set()
    for k in params:
        m = re.match(r'(VoiceData|MIDIChannel)(\d+)', k)
        if m:
            tg_numbers.add(int(m.group(2)))
    if not tg_numbers:
        tg_numbers = {1}  # Default to 1 if none found
    max_tg = max(tg_numbers)

    # MiniDexed TG parameter spec (see performanceconfig.cpp and official docs)
    tg_params = [
        ('BankNumber', 0, 127, 'int', '0'),
        ('VoiceNumber', 1, 32, 'int', '1'),
        ('MIDIChannel', 0, 255, 'int', '1'),
        ('Volume', 0, 127, 'int', '100'),
        ('Pan', 0, 127, 'int', '64'),
        ('Detune', -99, 99, 'int', '0'),
        ('Cutoff', 0, 99, 'int', '99'),
        ('Resonance', 0, 99, 'int', '0'),
        ('NoteLimitLow', 0, 127, 'int', '0'),
        ('NoteLimitHigh', 0, 127, 'int', '127'),
        ('NoteShift', -24, 24, 'int', '0'),
        ('ReverbSend', 0, 99, 'int', '50'),
        ('PitchBendRange', 0, 12, 'int', '2'),
        ('PitchBendStep', 0, 12, 'int', '0'),
        ('PortamentoMode', 0, 1, 'int', '0'),
        ('PortamentoGlissando', 0, 1, 'int', '0'),
        ('PortamentoTime', 0, 99, 'int', '0'),
        ('VoiceData', None, None, 'hex', ''),  # 156 hex bytes if present
        ('MonoMode', 0, 1, 'int', '0'),
        ('ModulationWheelRange', 0, 99, 'int', '99'),
        ('ModulationWheelTarget', 0, 7, 'int', '1'),
        ('FootControlRange', 0, 99, 'int', '99'),
        ('FootControlTarget', 0, 7, 'int', '0'),
        ('BreathControlRange', 0, 99, 'int', '99'),
        ('BreathControlTarget', 0, 7, 'int', '0'),
        ('AftertouchRange', 0, 99, 'int', '99'),
        ('AftertouchTarget', 0, 7, 'int', '0'),
    ]
    # Only check TGs present in the file
    for tg in sorted(tg_numbers):
        has_voicedata = f"VoiceData{tg}" in params and params[f"VoiceData{tg}"]
        has_bank = f"BankNumber{tg}" in params and params[f"BankNumber{tg}"]
        has_voice = f"VoiceNumber{tg}" in params and params[f"VoiceNumber{tg}"]
        if has_voicedata:
            # VoiceData present: BankNumber/VoiceNumber are ignored
            if has_bank or has_voice:
                errors.append(f"Warning: BankNumber{tg} and/or VoiceNumber{tg} are present but will not be used because VoiceData{tg} is present.")
        elif has_bank and has_voice:
            pass
        else:
            errors.append(f"Missing VoiceData{tg} or BankNumber{tg} and VoiceNumber{tg}")
        for param, minv, maxv, typ, default in tg_params:
            key = f"{param}{tg}"
            if param in ("VoiceData", "BankNumber", "VoiceNumber"):
                continue  # Already checked above
            if key not in params:
                errors.append(f"Missing {key}")
                continue
            value = params[key]
            if typ == 'int':
                try:
                    ival = int(value)
                    if ival < minv or ival > maxv:
                        errors.append(f"{key} out of range: {ival} (should be {minv}..{maxv})")
                except Exception:
                    errors.append(f"{key} not an integer: {value}")
            elif typ == 'hex':
                if value:
                    hexbytes = value.split()
                    if len(hexbytes) != 156:
                        errors.append(f"{key} should have 156 bytes, has {len(hexbytes)}")
                    for b in hexbytes:
                        if not re.fullmatch(r'[0-9A-Fa-f]{2}', b):
                            errors.append(f"{key} contains non-hex byte: {b}")
    # Global effects section (see MiniDexed spec)
    global_params = [
        ('CompressorEnable', 0, 1, 'int', '1'),
        ('ReverbEnable', 0, 1, 'int', '1'),
        ('ReverbSize', 0, 99, 'int', '70'),
        ('ReverbHighDamp', 0, 99, 'int', '50'),
        ('ReverbLowDamp', 0, 99, 'int', '50'),
        ('ReverbLowPass', 0, 99, 'int', '30'),
        ('ReverbDiffusion', 0, 99, 'int', '65'),
        ('ReverbLevel', 0, 99, 'int', '99'),
    ]
    for param, minv, maxv, typ, default in global_params:
        if param not in params:
            errors.append(f"Missing {param}")
            continue
        value = params[param]
        try:
            ival = int(value)
            if ival < minv or ival > maxv:
                errors.append(f"{param} out of range: {ival} (should be {minv}..{maxv})")
        except Exception:
            errors.append(f"{param} not an integer: {value}")
    return errors

def main():
    """
    Lint all .ini files in the given folder (default: tx816).
    Prints errors for each file, or 'All files OK.' if all pass.
    """
    folder = sys.argv[1] if len(sys.argv) > 1 else 'tx816'
    files = [f for f in os.listdir(folder) if f.endswith('.ini')]
    any_errors = False
    for f in sorted(files):
        path = os.path.join(folder, f)
        errors = lint_performance_ini(path)
        # --- Print summary for each file ---
        # Try to extract performance name from the first comment or filename
        perf_name = f
        with open(path, 'r') as fin:
            lines_raw = fin.readlines()
            for line in lines_raw:
                if line.strip().startswith('; MiniDexed Performance:'):
                    perf_name = line.strip().split(':',1)[-1].strip()
                    break
        # Now parse params as before
        params = dict()
        with open(path, 'r') as fin:
            lines = [line.strip() for line in fin if line.strip() and not line.strip().startswith(';')]
        for line in lines:
            if '=' in line:
                k, v = line.split('=', 1)
                params[k.strip()] = v.strip()
        # Find how many TGs are present by checking for VoiceDataN or MIDIChannelN keys
        tg_numbers = set()
        for k in params:
            m = re.match(r'(VoiceData|MIDIChannel)(\d+)', k)
            if m:
                tg_numbers.add(int(m.group(2)))
        if not tg_numbers:
            tg_numbers = {1}  # Default to 1 if none found
        # Print performance name above the table
        print(f"\n### {perf_name}\n")
        print(f"| TG | Pan  | MIDI Channel | Detune | Voice Name         | Comments              |")
        print(f"|----|------|--------------|--------|---------------------|-----------------------|")
        for tg in sorted(tg_numbers):
            pan = params.get(f'Pan{tg}', '?')
            midi = params.get(f'MIDIChannel{tg}', '?')
            detune = params.get(f'Detune{tg}', '?')
            vname = '?'
            vdata = params.get(f'VoiceData{tg}', None)
            comment = ''
            # Search for comment directly above the VoiceData line
            for i, line in enumerate(lines_raw):
                if line.strip().startswith(f'VoiceData{tg}='):
                    if i > 0 and lines_raw[i-1].strip().startswith(';'):
                        comment_line = lines_raw[i-1].strip().lstrip(';').strip()
                        if ' — ' in comment_line:
                            comment = comment_line.split(' — ', 1)[1].strip()
                        else:
                            comment = comment_line
                    break
            # Check if NoteLimitLow/High are set and add to comment
            nll = params.get(f'NoteLimitLow{tg}', None)
            nlh = params.get(f'NoteLimitHigh{tg}', None)
            if nll is not None and nlh is not None:
                nll_int = int(nll)
                nlh_int = int(nlh)
                import tx816
                nll_name = tx816.midi_number_to_note(nll_int)
                nlh_name = tx816.midi_number_to_note(nlh_int)
                if nll_int != 0 or nlh_int != 127:
                    note_comment = f"Limited from {nll_name} to {nlh_name}"
                    if comment:
                        comment += f"; {note_comment}"
                    else:
                        comment = note_comment

            if vdata:
                hexbytes = vdata.split()
                if len(hexbytes) >= 155:
                    try:
                        vced = [int(b, 16) for b in hexbytes[:155]]
                        vname = dx7.get_voice_name(vced).strip()
                        # Check for Aftertouch (P A.TCH != 0)
                        import tx816
                        match = next((v for v in tx816.function_data if v["Voice"].strip() == vname), None)
                        if match and str(match.get("P A.TCH", "0")) != "0":
                            if comment:
                                comment += "; Aftertouch"
                            else:
                                comment = "Aftertouch"
                    except Exception:
                        vname = '?'
            print(f"| {tg}  | {pan}   | {midi}           | {detune}     | {vname.ljust(19)}| {comment.ljust(21)}|")
        # --- End summary ---
        if errors:
            print(f"{f}:")
            for e in errors:
                print(f"  {e}")
            any_errors = True
    if not any_errors:
        print("All files OK.")

if __name__ == "__main__":
    main()
