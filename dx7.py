#!/usr/bin/env python3

# 'INIT VOICE' in VCED format
# 155 bytes
init_vced = [99, 99, 99, 99,                                                         # OP6 EG RATE 1-4 (0 to 99)
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
            0,                                                                       # ALGORITHM SELECT (0 to 31)
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
    return vmem

init_vmem = vced2vmem(init_vced)
print("Size of init_vmem: ", len(init_vmem))
# Print as decimal
for i in range(len(init_vmem)):
    print(init_vmem[i], end=", ")
print()

# 32 times init_vmem
init_vmem32 = init_vmem*32

print("Size of init_vmem32:", len(init_vmem32))

# Number of bytes in the sysex (= packed 32-voice data): 4104

# Make a sysex message from a bank of 32 VCED voices
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

    return sysex

# Make a bank of 32 VCED voices from a sysex message
def make_vced32(sysex):
    vced32 = []
    for i in range(7, 4111):
        vced32.append(sysex[i])
    return vced32

def make_init_vced32():
    # Make a sysex message containing 32 copies of the init voice converted to VMEM
    vmem = vced2vmem(init_vced)
    vmem32 = vmem*32
    sysex = make_sysex32(vmem32)
    return sysex

def main():
    print("Size of the init voice VCED:", len(init_vced))

    multiple_voices_sysex = make_init_vced32()
    print("Sysex message containing 32 copies of the init voice VCED converted to VMEM, length =", len(multiple_voices_sysex))

if __name__ == "__main__":
    main()
