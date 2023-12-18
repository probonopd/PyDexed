#!/usr/bin/env python3

# 'INIT VOICE' in VCED format
# 155 bytes
init_vced = [
            99, 99, 99, 99,                                                          # OP6 EG RATE 1-4 (0 to 99)
            99, 99, 99, 00,                                                          # OP6 EG LEVEL 1-4 (0 to 99)
            39,                                                                      # OP6 KEYBOARD LEVEL SCALING BREAK POINT (0 to 99)
            0,                                                                       # OP6 KEYBOARD LEVEL SCALING LEFT DEPTH (0 to 99)
            0,                                                                       # OP6 KEYBOARD LEVEL SCALING RIGHT DEPTH (0 to 99)
            0,                                                                       # OP6 KEYBOARD LEVEL SCALING LEFT CURVE (0 to 3)
            0,                                                                       # OP6 KEYBOARD LEVEL SCALING RIGHT CURVE (0 to 3)
            0,                                                                       # OP6 KEYBOARD RATE SCALING (0 to 7)
            0,                                                                       # OP6 AMPLITUDE MODULATION SENSITIVITY (0 to 3)
            0,                                                                       # OP6 KEY VELOCITY SENSITIVITY (0 to 7)
            0,                                                                       # OP6 OPERATOR OUTPUT LEVEL (0 to 99)
            0,                                                                       # OP6 OSCILLATOR MODE (0:RATIO, 1:FIXED)
            1,                                                                       # OP6 OSCILLATOR FREQUENCY COARSE (0 to 31)
            0,                                                                       # OP6 OSCILLATOR FREQUENCY FINE (0 to 99)
            7,                                                                       # OP6 OSCILLATOR DETUNE (0 to 14)
            99, 99, 99, 99, 99, 99, 99, 00, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7,  # OP5
            99, 99, 99, 99, 99, 99, 99, 00, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7,  # OP4
            99, 99, 99, 99, 99, 99, 99, 00, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7,  # OP3
            99, 99, 99, 99, 99, 99, 99, 00, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7,  # OP2
            99, 99, 99, 99, 99, 99, 99, 00, 39, 0, 0, 0, 0, 0, 0, 0, 99, 0, 1, 0, 7, # OP1
            99, 99, 99, 99,                                                          # PITCH EG RATE 1-4 (0 to 99)
            50, 50, 50, 50,                                                          # PITCH EG LEVEL 1-4 (0 to 99)
            31,                                                                      # ALGORITHM SELECT (0 to 31)
            0,                                                                       # FEEDBACK (0 to 7)
            1,                                                                       # OSCILLATOR KEY SYNC (0:OFF, 1:ON)
            35,                                                                      # LFO SPEED (0 to 99)
            0,                                                                       # LFO DELAY (0 to 99)
            0,                                                                       # LFO PITCH MODULATION DEPTH (0 to 99)
            0,                                                                       # LFO AMPLITUDE MODULATION DEPTH (0 to 99)
            1,                                                                       # LFO KEY SYNC (0:OFF, 1:ON)
            0,                                                                       # LFO WAVE (0:TRIANGLE, 1: SAW DOWN, 2:SAW UP, 3:SQUARE, 4:SINE, 5:SAMPLE&HOLD)
            3,                                                                       # LFO PITCH MODULATION SENSITIVITY (0 to 7)
            24,                                                                      # TRANSPOSE (0 to 48)
            73, 78, 73, 84, 32, 86, 79, 73, 67, 69                                   # 'INIT VOICE' ASCII string
            ] 

# Make a VCED voice from a sysex message
def make_vced(sysex):
    vced = []
    for i in range(7, 162):
        vced.append(sysex[i])
    assert len(vced) == 155
    return vced

def vced2vmem(vced):
    # Borrowed from https://github.com/rarepixel/dxconvert/blob/master/DXconvert/dx7.py
    vmem = [0]*128
    for op in range(6):
        for p in range(11):
            vmem[p+17*op] = vced[p+21*op] 
        vmem[11+17*op] = (vced[12+21*op]<<2) + vced[11+21*op] 
        vmem[12+17*op] = (vced[20+21*op]<<3) + vced[13+21*op] 
        vmem[13+17*op] = (vced[15+21*op]<<2) + vced[14+21*op]
        vmem[14+17*op] = vced[16+21*op]
        vmem[15+17*op] = (vced[18+21*op]<<1) + vced[17+21*op] 
        vmem[16+17*op] = vced[19+21*op]

    for p in range(102, 111):
        vmem[p] = vced[p+24]
    vmem[111] = vced[135] + (vced[136]<<3)
    for p in range(112, 116):
        vmem[p] = vced[p+25]
    vmem[116] = vced[141] + (vced[142]<<1) + (vced[143]<<4)
    for i in range(117, 128):
        vmem[i] = vced[i+27]
    for i in range(len(vmem)):
        vmem[i] = vmem[i]&127
    assert len(vmem) == 128
    return vmem


def vmem2vced(vmem):
    # Borrowed from https://github.com/rarepixel/dxconvert/blob/master/DXconvert/dx7.py
    vced=[0]*155
    for op in range(6):
        for p in range(11):
            vced[p+21*op] = vmem[p+17*op]&127
        vced[11+21*op] = vmem[11+17*op]&0b11
        vced[12+21*op] = (vmem[11+17*op]&0b1100)>>2
        vced[13+21*op] = vmem[12+17*op]&0b111
        vced[20+21*op] = (vmem[12+17*op]&0b1111000)>>3
        vced[14+21*op] = vmem[13+17*op]&0b11
        vced[15+21*op] = (vmem[13+17*op]&0b11100)>>2
        vced[16+21*op] = vmem[14+17*op]&127
        vced[17+21*op] = vmem[15+17*op]&1
        vced[18+21*op] = (vmem[15+17*op]&0b111110)>>1
        vced[19+21*op] = vmem[16+17*op]&127
    for p in range(102, 110):
        vced[p+24] = vmem[p]&127
    vced[134] = vmem[110]&0b11111
    vced[135] = vmem[111]&0b0111
    vced[136] = (vmem[111]&0b1000)>>3
    for p in range(112, 116):
        vced[p+25] = vmem[p]&127
    vced[141] = vmem[116]&1
    vced[142] = (vmem[116]&0b1110)>>1
    vced[143] = (vmem[116]&0b1110000)>>4
    for p in range(117, 128):
        vced[p+27] = vmem[p]
    for i in range(len(vced)):
        vced[i] = vced[i]&127
    assert len(vced) == 155
    return vced

init_vmem = vced2vmem(init_vced)

# 32 times init_vmem
init_vmem32 = init_vmem*32

# Make a sysex message from a bank of 32 voices
def make_sysex32(vced32):
    sysex = [0xF0, 0x43, 0x00, 0x09, 0x20, 0x00]
    for i in range(len(vced32)):
        sysex.append(vced32[i])
    # Caclulate checksum
    checksum = 0
    for i in range(6, len(sysex)):
        checksum += sysex[i]
    checksum = 128 - (128-sum(vced32)&127)%128 # TODO: Check whether this is correct
    sysex.append(checksum)
    sysex.append(0xF7)
    assert len(sysex) == 4104
    return sysex

# This can be used to get the currently selected voice from the bank of 32 voices
def get_vced_from_bank_sysex(sysex, voice_number):
    vmem = []
    vced = []
    for i in range(6 + 128*voice_number, 6 + 128*(voice_number+1)):
        vmem.append(sysex[i])
    assert len(vmem) == 128
    vced = vmem2vced(vmem)
    assert len(vced) == 155
    return vced

def make_init_bank_sysex():
    # Make a sysex message containing 32 copies of the init voice VCED converted to VMEM
    vmem = vced2vmem(init_vced)
    vmem32 = vmem*32
    bank_sysex = make_sysex32(vmem32)
    assert len(bank_sysex) == 4104
    return bank_sysex

def main():
    print("Size of the init voice VCED:", len(init_vced))

    multiple_voices_sysex = make_init_bank_sysex()
    print("Sysex message containing 32 copies of the init voice VCED converted to VMEM, length =", len(multiple_voices_sysex))

if __name__ == "__main__":
    main()
