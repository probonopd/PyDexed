#!/usr/bin/env python3

# Parse from Dexed XML to Python "Dexed state" dictionary and back

# TODO: Find out where the DX7 In and DX7 Out MIDI ports are stored, and handle them

import os, json

import xml.etree.ElementTree as ET

# From pip
import xmltodict

# Bundled
import codec

"""
This is how a Dexed state dictionary looks like:

{
    "dexedState": {
        "@cutoff": "1.0",
        "@reso": "0.0",
        "@gain": "1.0",
        "@currentProgram": "0",
        "@monoMode": "0",
        "@engineType": "1",
        "@masterTune": "0",
        "@opSwitch": "111111",
        "@transpose12AsScale": "1",
        "@mpeEnabled": "1",
        "@mpePitchBendRange": "24",
        "@wheelMod": "0 0 0 0",
        "@footMod": "0 0 0 0",
        "@breathMod": "0 0 0 0",
        "@aftertouchMod": "0 0 0 0",
        "@activeFileCartridge": "C:\\Users\\User\\AppData\\Roaming\\DigitalSuburban\\Dexed\\Cartridges\\Dexed_01.syx",
        "dexedBlob": {
            "@sysex": "F0 43 00 09 20 00 07 40 (...) F7",
            "@program": "07 40 2D 63 2D 63 00 00 (...) 00"
        },
        "midiCC": null
    }
}

Number of bytes in the sysex (= packed 32-voice data): 4104
Number of bytes in the program (= single voice data): 161
"""


def read_dexed_xml(data):
    """
    Reads a Dexed XML file and returns the parsed data as a Dexed state dictionary.

    Args:
        data (bytes): The Dexed XML file data.

    Returns:
        dict: The parsed Dexed XML data as a Dexed state dictionary.

    Raises:
        ValueError: If the XML data is invalid or cannot be parsed.

    """
    # Strip away the bytes before the initial "<?xml" string
    data = data[data.index(b'<?xml'):]

    # Replace "base64:" with nothing, this is a workaround for; xml.etree.ElementTree.ParseError: unbound prefix
    data = data.replace(b'base64:', b'')

    # Remove 0x00 byte and everything after it
    data = data[:data.index(b'\x00')]

    # Print
    print("XML data:")
    print(data.decode('utf-8'))

    # Parse the XML
    root = ET.fromstring(data, parser=ET.XMLParser(encoding='utf-8'))

    # Use xmltodict to convert the XML to a dictionary
    dexed_state_dict = xmltodict.parse(ET.tostring(root, encoding='utf-8'))

    # Get the encoded sysex from the dictionary
    encoded_sysex = dexed_state_dict['dexedState']['dexedBlob']['@sysex']

    # Decode the sysex
    decoded_sysex = codec.fromJuceBase64Encoding(encoded_sysex)
    
    # In the dictionary, replace the encoded sysex with the decoded sysex for better readability
    dexed_state_dict['dexedState']['dexedBlob']['@sysex'] = " ".join(decoded_sysex.hex().upper()[i:i+2] for i in range(0, len(decoded_sysex.hex()), 2))

    # Decode the program
    decoded_program = codec.fromJuceBase64Encoding(dexed_state_dict['dexedState']['dexedBlob']['@program'])

    # In the dictionary, replace the encoded program with the decoded program for better readability
    dexed_state_dict['dexedState']['dexedBlob']['@program'] = " ".join(decoded_program.hex().upper()[i:i+2] for i in range(0, len(decoded_program.hex()), 2))

    # Print the number of bytes in the decoded sysex and program
    # https://github.com/rarepixel/dxconvert/blob/master/FORMATS.txt
    # print("Number of bytes in the decoded sysex (= packed 32-voice data): " + str(len(decoded_sysex)))
    # print("Number of bytes in the decoded program (= single voice data): " + str(len(decoded_program)))

    # Assert that the number of bytes in the decoded sysex is 4104 and the number of bytes in the decoded program is 161
    assert len(decoded_sysex) == 4104
    assert len(decoded_program) == 161

    return dexed_state_dict

def construct_dexed_xml(dexed_state_dict):
    """
    Constructs a Dexed XML from a Dexed state dictionary.

    Args:
        dexed_state_dict (dict): The Dexed state dictionary.

    Returns:
        bytes: The Dexed XML data.

    Raises:
        ValueError: If the Dexed state dictionary is invalid or cannot be parsed.

    """
    # Get the encoded sysex from the dictionary
    decoded_sysex = dexed_state_dict['dexedState']['dexedBlob']['@sysex']

    # Encode the sysex
    encoded_sysex = codec.toJuceBase64Encoding(bytearray.fromhex(decoded_sysex.replace(' ', '')))

    # In the dictionary, replace the decoded sysex with the encoded sysex
    dexed_state_dict['dexedState']['dexedBlob']['@sysex'] = encoded_sysex

    # Get the encoded program from the dictionary
    decoded_program = dexed_state_dict['dexedState']['dexedBlob']['@program']

    # Encode the program
    encoded_program = codec.toJuceBase64Encoding(bytearray.fromhex(decoded_program.replace(' ', '')))

    # In the dictionary, replace the decoded program with the encoded program
    dexed_state_dict['dexedState']['dexedBlob']['@program'] = encoded_program

    # Convert the dictionary to XML
    xml = xmltodict.unparse(dexed_state_dict, pretty=False).replace('sysex', 'base64:sysex').replace('program', 'base64:program').replace('\n', ' ')

    # Some fixes for the XML to make it identical to the original XML
    xml = xml.replace('<midiCC></midiCC>', '<midiCC/>')
    xml = xml.replace('></dexedBlob>', '/>')
    xml = xml.replace('utf-8', 'UTF-8')

    return xml

def main():
    # Open the Dexed state file 'savedstate.dexed', it is a Dexed project state file from the standalone version of Dexed
    with open(os.path.dirname(__file__) + '/savedstate.dexed', 'rb') as f:
        data = f.read()
    dexed_state_dict = read_dexed_xml(data)

    # Pretty print the dictionary
    print(json.dumps(dexed_state_dict, indent=4))

    # From the dictionary, construct a Dexed XML file
    encoded_xml = construct_dexed_xml(dexed_state_dict)

    # For comparison, get <?xml ...</dexedState> from the original Dexed XML file
    original_data = data[data.index(b'<?xml'):data.index(b'</dexedState>') + len('</dexedState>')]

    # Compare the original XML with the constructed XML
    if original_data.decode('utf-8') == encoded_xml:
        print("Original XML and constructed XML are identical.")
    else:
        print("Original XML and constructed XML are NOT identical.")

    
if __name__ == '__main__':
    main()