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

class vced:

    def __init__(self, vced):
        self.op6egrate1 = 99
        self.op6egrate2 = 99
        self.op6egrate3 = 99
        self.op6egrate4 = 99
        self.op6elevel1 = 99
        self.op6elevel2 = 99
        self.op6elevel3 = 99
        self.op6elevel4 = 0
        self.op6ksbreakpoint = 39
        self.op6ksleftdepth = 0
        self.op6ksrightdepth = 0
        self.op6ksleftcurve = 0
        self.op6ksrightcurve = 0
        self.op6krs = 0
        self.op6ams = 0
        self.op6keyvelsens = 0
        self.op6outputlevel = 0
        self.op6oscmode = 0
        self.op6osccoarse = 1
        self.op6oscfine = 0
        self.op6detune = 7
        self.op5egrate1 = 99
        self.op5egrate2 = 99
        self.op5egrate3 = 99
        self.op5egrate4 = 99
        self.op5elevel1 = 99
        self.op5elevel2 = 99
        self.op5elevel3 = 99
        self.op5elevel4 = 0
        self.op5ksbreakpoint = 39
        self.op5ksleftdepth = 0
        self.op5ksrightdepth = 0
        self.op5ksleftcurve = 0
        self.op5ksrightcurve = 0
        self.op5krs = 0
        self.op5ams = 0
        self.op5keyvelsens = 0
        self.op5outputlevel = 0
        self.op5oscmode = 0
        self.op5osccoarse = 1
        self.op5oscfine = 0
        self.op5detune = 7
        self.op4egrate1 = 99
        self.op4egrate2 = 99
        self.op4egrate3 = 99
        self.op4egrate4 = 99
        self.op4elevel1 = 99
        self.op4elevel2 = 99
        self.op4elevel3 = 99
        self.op4elevel4 = 0
        self.op4ksbreakpoint = 39
        self.op4ksleftdepth = 0
        self.op4ksrightdepth = 0
        self.op4ksleftcurve = 0
        self.op4ksrightcurve = 0
        self.op4krs = 0
        self.op4ams = 0
        self.op4keyvelsens = 0
        self.op4outputlevel = 0
        self.op4oscmode = 0
        self.op4osccoarse = 1
        self.op4oscfine = 0
        self.op4detune = 7
        self.op3egrate1 = 99
        self.op3egrate2 = 99
        self.op3egrate3 = 99
        self.op3egrate4 = 99
        self.op3elevel1 = 99
        self.op3elevel2 = 99
        self.op3elevel3 = 99
        self.op3elevel4 = 0
        self.op3ksbreakpoint = 39
        self.op3ksleftdepth = 0
        self.op3ksrightdepth = 0
        self.op3ksleftcurve = 0
        self.op3ksrightcurve = 0
        self.op3krs = 0
        self.op3ams = 0
        self.op3keyvelsens = 0
        self.op3outputlevel = 0
        self.op3oscmode = 0
        self.op3osccoarse = 1
        self.op3oscfine = 0
        self.op3detune = 7
        self.op2egrate1 = 99
        self.op2egrate2 = 99
        self.op2egrate3 = 99
        self.op2egrate4 = 99
        self.op2elevel1 = 99
        self.op2elevel2 = 99
        self.op2elevel3 = 99
        self.op2elevel4 = 0
        self.op2ksbreakpoint = 39
        self.op2ksleftdepth = 0
        self.op2ksrightdepth = 0
        self.op2ksleftcurve = 0
        self.op2ksrightcurve = 0
        self.op2krs = 0
        self.op2ams = 0
        self.op2keyvelsens = 0
        self.op2outputlevel = 0
        self.op2oscmode = 0
        self.op2osccoarse = 1
        self.op2oscfine = 0
        self.op2detune = 7
        self.op1egrate1 = 99
        self.op1egrate2 = 99
        self.op1egrate3 = 99
        self.op1egrate4 = 99
        self.op1elevel1 = 99
        self.op1elevel2 = 99
        self.op1elevel3 = 99
        self.op1elevel4 = 0
        self.op1ksbreakpoint = 39
        self.op1ksleftdepth = 0
        self.op1ksrightdepth = 0
        self.op1ksleftcurve = 0
        self.op1ksrightcurve = 0
        self.op1krs = 0
        self.op1ams = 0
        self.op1keyvelsens = 0
        self.op1outputlevel = 0
        self.op1oscmode = 0
        self.op1osccoarse = 1
        self.op1oscfine = 0
        self.op1detune = 7
        self.pitchegrate1 = 99
        self.pitchegrate2 = 99
        self.pitchegrate3 = 99
        self.pitchegrate4 = 99
        self.pitchelevel1 = 99
        self.pitchelevel2 = 99
        self.pitchelevel3 = 99
        self.pitchelevel4 = 99
        self.algorithm = 31
        self.feedback = 0
        self.osckeysync = 1
        self.lfospeed = 35
        self.lfodelay = 0
        self.lfopitchmoddepth = 0
        self.lfoampmoddepth = 0
        self.lfokeysync = 1
        self.lfowave = 0
        self.lfopitchmodsens = 3
        self.transpose = 24
        self.name = "INIT VOICE" # 10 characters

    def get_bytes(self):
        # 155 bytes
        bytes = []
        for field in [
            self.op6egrate1, self.op6egrate2, self.op6egrate3, self.op6egrate4,
            self.op6elevel1, self.op6elevel2, self.op6elevel3, self.op6elevel4,
            self.op6ksbreakpoint,
            self.op6ksleftdepth,
            self.op6ksrightdepth,
            self.op6ksleftcurve,
            self.op6ksrightcurve,
            self.op6krs,
            self.op6ams,
            self.op6keyvelsens,
            self.op6outputlevel,
            self.op6oscmode,
            self.op6osccoarse,
            self.op6oscfine,
            self.op6detune,
            self.op5egrate1, self.op5egrate2, self.op5egrate3, self.op5egrate4,
            self.op5elevel1, self.op5elevel2, self.op5elevel3, self.op5elevel4,
            self.op5ksbreakpoint,
            self.op5ksleftdepth,
            self.op5ksrightdepth,
            self.op5ksleftcurve,
            self.op5ksrightcurve,
            self.op5krs,
            self.op5ams,
            self.op5keyvelsens,
            self.op5outputlevel,
            self.op5oscmode,
            self.op5osccoarse,
            self.op5oscfine,
            self.op5detune,
            self.op4egrate1, self.op4egrate2, self.op4egrate3, self.op4egrate4,
            self.op4elevel1, self.op4elevel2, self.op4elevel3, self.op4elevel4,
            self.op4ksbreakpoint,
            self.op4ksleftdepth,
            self.op4ksrightdepth,
            self.op4ksleftcurve,
            self.op4ksrightcurve,
            self.op4krs,
            self.op4ams,
            self.op4keyvelsens,
            self.op4outputlevel,
            self.op4oscmode,
            self.op4osccoarse,
            self.op4oscfine,
            self.op4detune,
            self.op3egrate1, self.op3egrate2, self.op3egrate3, self.op3egrate4,
            self.op3elevel1, self.op3elevel2, self.op3elevel3, self.op3elevel4,
            self.op3ksbreakpoint,
            self.op3ksleftdepth,
            self.op3ksrightdepth,
            self.op3ksleftcurve,
            self.op3ksrightcurve,
            self.op3krs,
            self.op3ams,
            self.op3keyvelsens,
            self.op3outputlevel,
            self.op3oscmode,
            self.op3osccoarse,
            self.op3oscfine,
            self.op3detune,
            self.op2egrate1, self.op2egrate2, self.op2egrate3, self.op2egrate4,
            self.op2elevel1, self.op2elevel2, self.op2elevel3, self.op2elevel4,
            self.op2ksbreakpoint,
            self.op2ksleftdepth,
            self.op2ksrightdepth,
            self.op2ksleftcurve,
            self.op2ksrightcurve,
            self.op2krs,
            self.op2ams,
            self.op2keyvelsens,
            self.op2outputlevel,
            self.op2oscmode,
            self.op2osccoarse,
            self.op2oscfine,
            self.op2detune,
            self.op1egrate1, self.op1egrate2, self.op1egrate3, self.op1egrate4,
            self.op1elevel1, self.op1elevel2, self.op1elevel3, self.op1elevel4,
            self.op1ksbreakpoint,
            self.op1ksleftdepth,
            self.op1ksrightdepth,
            self.op1ksleftcurve,
            self.op1ksrightcurve,
            self.op1krs,
            self.op1ams,
            self.op1keyvelsens,
            self.op1outputlevel,
            self.op1oscmode,
            self.op1osccoarse,
            self.op1oscfine,
            self.op1detune,
            self.pitchegrate1, self.pitchegrate2, self.pitchegrate3, self.pitchegrate4,
            self.pitchelevel1, self.pitchelevel2, self.pitchelevel3, self.pitchelevel4,
            self.algorithm,
            self.feedback,
            self.osckeysync,
            self.lfospeed,
            self.lfodelay,
            self.lfopitchmoddepth,
            self.lfoampmoddepth,
            self.lfokeysync,
            self.lfowave,
            self.lfopitchmodsens,
            self.transpose,
            ]:
            bytes.append(field)
        for i in range(10):
            bytes.append(ord(self.name[i]))
        assert len(bytes) == 155
        return bytes
    
    def set_bytes(self, bytes):
        assert len(bytes) == 155
        self.op6egrate1 = bytes[0]
        self.op6egrate2 = bytes[1]
        self.op6egrate3 = bytes[2]
        self.op6egrate4 = bytes[3]
        self.op6elevel1 = bytes[4]
        self.op6elevel2 = bytes[5]
        self.op6elevel3 = bytes[6]
        self.op6elevel4 = bytes[7]
        self.op6ksbreakpoint = bytes[8]
        self.op6ksleftdepth = bytes[9]
        self.op6ksrightdepth = bytes[10]
        self.op6ksleftcurve = bytes[11]
        self.op6ksrightcurve = bytes[12]
        self.op6krs = bytes[13]
        self.op6ams = bytes[14]
        self.op6keyvelsens = bytes[15]
        self.op6outputlevel = bytes[16]
        self.op6oscmode = bytes[17]
        self.op6osccoarse = bytes[18]
        self.op6oscfine = bytes[19]
        self.op6detune = bytes[20]
        self.op5egrate1 = bytes[21]
        self.op5egrate2 = bytes[22]
        self.op5egrate3 = bytes[23]
        self.op5egrate4 = bytes[24]
        self.op5elevel1 = bytes[25]
        self.op5elevel2 = bytes[26]
        self.op5elevel3 = bytes[27]
        self.op5elevel4 = bytes[28]
        self.op5ksbreakpoint = bytes[29]
        self.op5ksleftdepth = bytes[30]
        self.op5ksrightdepth = bytes[31]
        self.op5ksleftcurve = bytes[32]
        self.op5ksrightcurve = bytes[33]
        self.op5krs = bytes[34]
        self.op5ams = bytes[35]
        self.op5keyvelsens = bytes[36]
        self.op5outputlevel = bytes[37]
        self.op5oscmode = bytes[38]
        self.op5osccoarse = bytes[39]
        self.op5oscfine = bytes[40]
        self.op5detune = bytes[41]
        self.op4egrate1 = bytes[42]
        self.op4egrate2 = bytes[43]
        self.op4egrate3 = bytes[44]
        self.op4egrate4 = bytes[45]
        self.op4elevel1 = bytes[46]
        self.op4elevel2 = bytes[47]
        self.op4elevel3 = bytes[48]
        self.op4elevel4 = bytes[49]
        self.op4ksbreakpoint = bytes[50]
        self.op4ksleftdepth = bytes[51]
        self.op4ksrightdepth = bytes[52]
        self.op4ksleftcurve = bytes[53]
        self.op4ksrightcurve = bytes[54]
        self.op4krs = bytes[55]
        self.op4ams = bytes[56]
        self.op4keyvelsens = bytes[57]
        self.op4outputlevel = bytes[58]
        self.op4oscmode = bytes[59]
        self.op4osccoarse = bytes[60]
        self.op4oscfine = bytes[61]
        self.op4detune = bytes[62]
        self.op3egrate1 = bytes[63]
        self.op3egrate2 = bytes[64]
        self.op3egrate3 = bytes[65]
        self.op3egrate4 = bytes[66]
        self.op3elevel1 = bytes[67]
        self.op3elevel2 = bytes[68]
        self.op3elevel3 = bytes[69]
        self.op3elevel4 = bytes[70]
        self.op3ksbreakpoint = bytes[71]
        self.op3ksleftdepth = bytes[72]
        self.op3ksrightdepth = bytes[73]
        self.op3ksleftcurve = bytes[74]
        self.op3ksrightcurve = bytes[75]
        self.op3krs = bytes[76]
        self.op3ams = bytes[77]
        self.op3keyvelsens = bytes[78]
        self.op3outputlevel = bytes[79]
        self.op3oscmode = bytes[80]
        self.op3osccoarse = bytes[81]
        self.op3oscfine = bytes[82]
        self.op3detune = bytes[83]
        self.op2egrate1 = bytes[84]
        self.op2egrate2 = bytes[85]
        self.op2egrate3 = bytes[86]
        self.op2egrate4 = bytes[87]
        self.op2elevel1 = bytes[88]
        self.op2elevel2 = bytes[89]
        self.op2elevel3 = bytes[90]
        self.op2elevel4 = bytes[91]
        self.op2ksbreakpoint = bytes[92]
        self.op2ksleftdepth = bytes[93]
        self.op2ksrightdepth = bytes[94]
        self.op2ksleftcurve = bytes[95]
        self.op2ksrightcurve = bytes[96]
        self.op2krs = bytes[97]
        self.op2ams = bytes[98]
        self.op2keyvelsens = bytes[99]
        self.op2outputlevel = bytes[100]
        self.op2oscmode = bytes[101]
        self.op2osccoarse = bytes[102]
        self.op2oscfine = bytes[103]
        self.op2detune = bytes[104]
        self.op1egrate1 = bytes[105]
        self.op1egrate2 = bytes[106]
        self.op1egrate3 = bytes[107]
        self.op1egrate4 = bytes[108]
        self.op1elevel1 = bytes[109]
        self.op1elevel2 = bytes[110]
        self.op1elevel3 = bytes[111]
        self.op1elevel4 = bytes[112]
        self.op1ksbreakpoint = bytes[113]
        self.op1ksleftdepth = bytes[114]
        self.op1ksrightdepth = bytes[115]
        self.op1ksleftcurve = bytes[116]
        self.op1ksrightcurve = bytes[117]
        self.op1krs = bytes[118]
        self.op1ams = bytes[119]
        self.op1keyvelsens = bytes[120]
        self.op1outputlevel = bytes[121]
        self.op1oscmode = bytes[122]
        self.op1osccoarse = bytes[123]
        self.op1oscfine = bytes[124]
        self.op1detune = bytes[125]
        self.pitchegrate1 = bytes[126]
        self.pitchegrate2 = bytes[127]
        self.pitchegrate3 = bytes[128]
        self.pitchegrate4 = bytes[129]
        self.pitchelevel1 = bytes[130]
        self.pitchelevel2 = bytes[131]
        self.pitchelevel3 = bytes[132]
        self.pitchelevel4 = bytes[133]
        self.algorithm = bytes[134]
        self.feedback = bytes[135]
        self.osckeysync = bytes[136]
        self.lfospeed = bytes[137]
        self.lfodelay = bytes[138]
        self.lfopitchmoddepth = bytes[139]
        self.lfoampmoddepth = bytes[140]
        self.lfokeysync = bytes[141]
        self.lfowave = bytes[142]
        self.lfopitchmodsens = bytes[143]
        self.transpose = bytes[144]
        self.name = ""
        for i in range(10):
            self.name += chr(bytes[145+i])
        assert len(self.name) == 10
        assert len(bytes) == 155
        return bytes

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

# Get the name of a voice from a VCED
def get_voice_name(vced):
    name = ""
    for i in range(145, 155):
        name += chr(vced[i])
    # Make a string that is 10 characters long, padded with spaces
    name = name.ljust(10)
    assert len(name) == 10
    return name

# Load a VCED from a file containing 32 voices (e.g. a sysex file)
def load_vced_from_file(path, voice_number):
    with open(path, 'rb') as f:
        sysex = f.read()
    vced = get_vced_from_bank_sysex(sysex, voice_number)
    return vced

def main():
    print("Size of the init voice VCED:", len(init_vced))

    multiple_voices_sysex = make_init_bank_sysex()
    print("Sysex message containing 32 copies of the init voice VCED converted to VMEM, length =", len(multiple_voices_sysex))

if __name__ == "__main__":
    main()
